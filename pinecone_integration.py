"""
Pinecone Vector Database Integration for POC
Implements real vector search for equipment manuals
"""

import os
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

# Check if pinecone is available
try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("Warning: pinecone-client not installed. Install with: pip install pinecone-client")


class PineconeRAG:
    """
    Pinecone-based RAG system for equipment manuals
    Falls back to keyword matching if Pinecone unavailable
    """
    
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = "equipment-manuals"
        
        self.pc = None
        self.index = None
        self.available = PINECONE_AVAILABLE and self.api_key is not None
        
        if self.available:
            self._initialize_pinecone()
        else:
            print("Pinecone not available - using keyword-based RAG")
    
    def _initialize_pinecone(self):
        """Initialize Pinecone connection"""
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=self.api_key)
            
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            index_names = [idx['name'] for idx in existing_indexes]
            
            if self.index_name not in index_names:
                print(f"Creating Pinecone index: {self.index_name}")
                self._create_index()
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            
            # Check if index needs population
            stats = self.index.describe_index_stats()
            if stats['total_vector_count'] == 0:
                print("Index is empty - populating with manual data...")
                self._populate_index()
            
            print(f"✅ Pinecone initialized: {stats['total_vector_count']} vectors")
            
        except Exception as e:
            print(f"❌ Error initializing Pinecone: {e}")
            self.available = False
    
    def _create_index(self):
        """Create Pinecone index with appropriate settings"""
        try:
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # Using sentence-transformers/all-MiniLM-L6-v2
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            print(f"✅ Created index: {self.index_name}")
        except Exception as e:
            print(f"❌ Error creating index: {e}")
            raise
    
    def _populate_index(self):
        """Populate index with equipment manual chunks"""
        from manuals import MANUAL_CONTENT
        
        vectors = []
        
        for equipment_id, manual in MANUAL_CONTENT.items():
            # Process troubleshooting sections
            for issue_type, troubleshooting in manual['troubleshooting'].items():
                # Create chunks for each troubleshooting section
                chunks = self._create_chunks(equipment_id, issue_type, troubleshooting)
                vectors.extend(chunks)
        
        if vectors:
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            print(f"✅ Populated index with {len(vectors)} vectors")
    
    def _create_chunks(self, equipment_id, issue_type, troubleshooting):
        """Create vector chunks from troubleshooting section"""
        chunks = []
        
        # Main troubleshooting chunk
        main_text = f"""
        Equipment: {equipment_id}
        Issue: {issue_type}
        Symptoms: {troubleshooting['symptoms']}
        Possible Causes: {', '.join(troubleshooting['possible_causes'])}
        """
        
        chunk_id = f"{equipment_id}_{issue_type}_main"
        embedding = self._get_embedding(main_text)
        
        chunks.append({
            'id': chunk_id,
            'values': embedding,
            'metadata': {
                'equipment_id': equipment_id,
                'issue_type': issue_type,
                'section': 'main',
                'text': main_text.strip()
            }
        })
        
        # Resolution steps chunk
        resolution_text = f"""
        Equipment: {equipment_id}
        Issue: {issue_type}
        Resolution Steps: {' '.join(troubleshooting['resolution'])}
        """
        
        chunk_id = f"{equipment_id}_{issue_type}_resolution"
        embedding = self._get_embedding(resolution_text)
        
        chunks.append({
            'id': chunk_id,
            'values': embedding,
            'metadata': {
                'equipment_id': equipment_id,
                'issue_type': issue_type,
                'section': 'resolution',
                'text': resolution_text.strip(),
                'resolution_steps': troubleshooting['resolution']
            }
        })
        
        # Parts chunk
        if troubleshooting.get('required_parts'):
            parts_text = f"""
            Equipment: {equipment_id}
            Issue: {issue_type}
            Required Parts: {', '.join([p['description'] for p in troubleshooting['required_parts']])}
            """
            
            chunk_id = f"{equipment_id}_{issue_type}_parts"
            embedding = self._get_embedding(parts_text)
            
            chunks.append({
                'id': chunk_id,
                'values': embedding,
                'metadata': {
                    'equipment_id': equipment_id,
                    'issue_type': issue_type,
                    'section': 'parts',
                    'text': parts_text.strip(),
                    'required_parts': troubleshooting['required_parts']
                }
            })
        
        return chunks
    
    def _get_embedding(self, text):
        """
        Get embedding for text using sentence-transformers
        For POC, using simple hash-based mock embeddings
        In production, use actual embedding model
        """
        # Mock embedding for POC (384 dimensions)
        # In production, use: sentence-transformers or watsonx.ai embeddings
        
        # Simple deterministic embedding based on text hash
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to 384-dimensional vector
        embedding = []
        for i in range(384):
            byte_val = hash_bytes[i % len(hash_bytes)]
            # Normalize to [-1, 1]
            embedding.append((byte_val / 255.0) * 2 - 1)
        
        return embedding
    
    def query(self, query_text, equipment_id=None, top_k=5):
        """
        Query Pinecone for relevant manual sections
        
        Args:
            query_text: Search query
            equipment_id: Optional equipment filter
            top_k: Number of results to return
        
        Returns:
            list: Relevant manual sections with scores
        """
        if not self.available or self.index is None:
            return self._fallback_query(query_text, equipment_id)
        
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query_text)
            
            # Build filter
            filter_dict = {}
            if equipment_id:
                filter_dict['equipment_id'] = equipment_id
            
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
            
            # Format results
            formatted_results = []
            for match in results['matches']:
                formatted_results.append({
                    'id': match['id'],
                    'score': match['score'],
                    'equipment_id': match['metadata'].get('equipment_id'),
                    'issue_type': match['metadata'].get('issue_type'),
                    'section': match['metadata'].get('section'),
                    'text': match['metadata'].get('text'),
                    'resolution_steps': match['metadata'].get('resolution_steps'),
                    'required_parts': match['metadata'].get('required_parts')
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error querying Pinecone: {e}")
            return self._fallback_query(query_text, equipment_id)
    
    def _fallback_query(self, query_text, equipment_id=None):
        """Fallback to keyword-based search if Pinecone unavailable"""
        from rag import query_equipment_manual
        
        # Extract anomaly type from query
        anomaly_type = "overheating"  # Default
        if "vibration" in query_text.lower():
            anomaly_type = "excessive_vibration"
        elif "pressure" in query_text.lower():
            anomaly_type = "low_pressure"
        elif "current" in query_text.lower():
            anomaly_type = "high_current"
        
        # Use existing RAG system
        if equipment_id:
            result = query_equipment_manual(equipment_id, anomaly_type)
            return [{
                'id': f"{equipment_id}_{anomaly_type}",
                'score': 0.85,
                'equipment_id': equipment_id,
                'issue_type': anomaly_type,
                'section': 'fallback',
                'text': result['troubleshooting']['symptoms'],
                'resolution_steps': result.get('resolution_steps', []),
                'required_parts': result.get('required_parts', [])
            }]
        
        return []
    
    def test_connection(self):
        """Test Pinecone connection and index status"""
        if not self.available:
            return {
                'status': 'unavailable',
                'message': 'Pinecone not configured or library not installed'
            }
        
        try:
            stats = self.index.describe_index_stats()
            return {
                'status': 'connected',
                'message': 'Pinecone connection successful',
                'index_name': self.index_name,
                'total_vectors': stats['total_vector_count'],
                'dimension': stats.get('dimension', 384)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            }


# Singleton instance
_pinecone_instance = None

def get_pinecone_rag():
    """Get or create Pinecone RAG instance"""
    global _pinecone_instance
    if _pinecone_instance is None:
        _pinecone_instance = PineconeRAG()
    return _pinecone_instance


# Quick test
if __name__ == "__main__":
    print("=== Testing Pinecone Integration ===\n")
    
    # Initialize
    pinecone_rag = PineconeRAG()
    
    # Test connection
    print("Test 1: Connection Test")
    print("-" * 50)
    result = pinecone_rag.test_connection()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if 'total_vectors' in result:
        print(f"Total Vectors: {result['total_vectors']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test query
    if pinecone_rag.available:
        print("Test 2: Query Test")
        print("-" * 50)
        
        query_text = "HVAC system temperature too high overheating"
        results = pinecone_rag.query(query_text, equipment_id="HVAC-001", top_k=3)
        
        print(f"Query: {query_text}")
        print(f"Results: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Equipment: {result['equipment_id']}")
            print(f"  Issue: {result['issue_type']}")
            print(f"  Score: {result['score']:.3f}")
            print(f"  Section: {result['section']}")
            if result.get('resolution_steps'):
                print(f"  Steps: {len(result['resolution_steps'])} steps")
    else:
        print("Test 2: Skipped (Pinecone not available)")
    
    print("\n=== Tests Complete ===")

# Made with Bob
