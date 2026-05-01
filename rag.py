"""
Mock RAG (Retrieval-Augmented Generation) system for POC
Task 3: 1.5 hours - Simple keyword matching, no Pinecone needed initially
Updated: Added Pinecone vector database integration
"""

from manuals import get_manual, get_troubleshooting_section, search_manual_content

# Import Pinecone integration
try:
    from pinecone_integration import get_pinecone_rag
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("Pinecone integration not available - using keyword matching")


class MockRAG:
    """
    RAG implementation with optional Pinecone vector database
    Falls back to keyword matching if Pinecone unavailable
    """
    
    def __init__(self, use_pinecone=False):
        self.manuals_loaded = True
        self.use_pinecone = use_pinecone
        self.pinecone_rag = None
        
        if use_pinecone and PINECONE_AVAILABLE:
            self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone RAG"""
        try:
            self.pinecone_rag = get_pinecone_rag()
            if self.pinecone_rag.available:
                print("✅ Pinecone RAG initialized")
                self.use_pinecone = True
            else:
                print("⚠️  Pinecone not available, using keyword matching")
                self.use_pinecone = False
        except Exception as e:
            print(f"❌ Error initializing Pinecone: {e}")
            self.use_pinecone = False
    
    def query_manual(self, equipment_id, anomaly_type, sensor_data=None):
        """
        Query equipment manual for troubleshooting information
        Uses Pinecone if available, falls back to keyword matching
        
        Args:
            equipment_id: Equipment identifier (e.g., 'HVAC-001')
            anomaly_type: Type of anomaly (e.g., 'overheating', 'excessive_vibration')
            sensor_data: Optional sensor readings for context
        
        Returns:
            dict: Relevant manual sections and troubleshooting info
        """
        # Try Pinecone first if enabled
        if self.use_pinecone and self.pinecone_rag and self.pinecone_rag.available:
            try:
                return self._query_with_pinecone(equipment_id, anomaly_type, sensor_data)
            except Exception as e:
                print(f"⚠️  Pinecone query failed: {e}, falling back to keyword matching")
        
        # Fall back to keyword matching
        return self._query_with_keywords(equipment_id, anomaly_type, sensor_data)
    
    def _query_with_pinecone(self, equipment_id, anomaly_type, sensor_data):
        """Query using Pinecone vector database"""
        # Build query text
        query_parts = [f"Equipment {equipment_id}", f"Issue: {anomaly_type}"]
        if sensor_data:
            query_parts.append(f"Sensors: {self._format_sensor_context(sensor_data)}")
        query_text = " ".join(query_parts)
        
        # Query Pinecone
        results = self.pinecone_rag.query(query_text, equipment_id=equipment_id, top_k=3)
        
        if not results:
            # Fall back to keyword matching
            return self._query_with_keywords(equipment_id, anomaly_type, sensor_data)
        
        # Get manual for additional context
        manual = get_manual(equipment_id)
        
        # Combine Pinecone results
        combined_resolution_steps = []
        combined_parts = []
        relevant_sections = []
        
        for result in results:
            if result.get('resolution_steps'):
                combined_resolution_steps.extend(result['resolution_steps'])
            if result.get('required_parts'):
                combined_parts.extend(result['required_parts'])
            
            relevant_sections.append({
                "section": result.get('section', 'unknown'),
                "issue_type": result.get('issue_type', anomaly_type),
                "content": result.get('text', ''),
                "relevance_score": result.get('score', 0.0)
            })
        
        # Remove duplicates
        combined_resolution_steps = list(dict.fromkeys(combined_resolution_steps))
        
        # Get primary troubleshooting section
        troubleshooting = get_troubleshooting_section(equipment_id, anomaly_type)
        
        return {
            "equipment_id": equipment_id,
            "equipment_name": manual["equipment_name"],
            "equipment_type": manual["equipment_type"],
            "anomaly_type": anomaly_type,
            "troubleshooting": troubleshooting,
            "relevant_sections": relevant_sections,
            "required_parts": combined_parts if combined_parts else troubleshooting.get("required_parts", []),
            "resolution_steps": combined_resolution_steps if combined_resolution_steps else troubleshooting.get("resolution", []),
            "estimated_time": troubleshooting.get("estimated_time", "Unknown"),
            "safety_precautions": troubleshooting.get("safety_precautions", []),
            "diagnosis_steps": troubleshooting.get("diagnosis_steps", []),
            "possible_causes": troubleshooting.get("possible_causes", []),
            "query_method": "pinecone"
        }
    
    def _query_with_keywords(self, equipment_id, anomaly_type, sensor_data):
        """Query using keyword matching (original implementation)"""
        try:
            # Get the manual
            manual = get_manual(equipment_id)
            
            # Map anomaly types to troubleshooting sections
            anomaly_mapping = {
                'overheating': 'overheating',
                'high_temperature': 'overheating',
                'excessive_vibration': 'excessive_vibration',
                'high_vibration': 'excessive_vibration',
                'low_pressure': 'low_pressure',
                'pressure_drop': 'low_pressure',
                'high_current': 'high_current',
                'overcurrent': 'high_current'
            }
            
            # Get the appropriate troubleshooting section
            mapped_issue = anomaly_mapping.get(anomaly_type.lower(), anomaly_type.lower())
            troubleshooting = get_troubleshooting_section(equipment_id, mapped_issue)
            
            # Extract key information
            result = {
                "equipment_id": equipment_id,
                "equipment_name": manual["equipment_name"],
                "equipment_type": manual["equipment_type"],
                "anomaly_type": anomaly_type,
                "troubleshooting": troubleshooting,
                "relevant_sections": [
                    {
                        "section": "troubleshooting",
                        "issue_type": mapped_issue,
                        "content": troubleshooting["symptoms"],
                        "relevance_score": 0.95
                    }
                ],
                "required_parts": troubleshooting.get("required_parts", []),
                "resolution_steps": troubleshooting.get("resolution", []),
                "estimated_time": troubleshooting.get("estimated_time", "Unknown"),
                "safety_precautions": troubleshooting.get("safety_precautions", []),
                "diagnosis_steps": troubleshooting.get("diagnosis_steps", []),
                "possible_causes": troubleshooting.get("possible_causes", [])
            }
            
            # Add sensor context if provided
            if sensor_data:
                result["sensor_context"] = self._format_sensor_context(sensor_data)
            
            return result
            
        except Exception as e:
            # Fallback response if something goes wrong
            return {
                "equipment_id": equipment_id,
                "anomaly_type": anomaly_type,
                "error": str(e),
                "troubleshooting": {
                    "symptoms": f"Anomaly detected: {anomaly_type}",
                    "possible_causes": ["Unknown - requires manual inspection"],
                    "resolution": ["Contact maintenance technician"],
                    "required_parts": [],
                    "estimated_time": "Unknown"
                },
                "required_parts": [],
                "resolution_steps": ["Contact maintenance technician for inspection"],
                "estimated_time": "Unknown"
            }
    
    def _format_sensor_context(self, sensor_data):
        """Format sensor data for context"""
        context = []
        for key, value in sensor_data.items():
            if key != 'time' and key != 'status':
                context.append(f"{key}: {value}")
        return ", ".join(context)
    
    def search_by_keywords(self, equipment_id, keywords):
        """
        Search manual by keywords (simple implementation)
        
        Args:
            equipment_id: Equipment identifier
            keywords: List of keywords or single keyword string
        
        Returns:
            list: Matching sections
        """
        if isinstance(keywords, str):
            keywords = [keywords]
        
        results = []
        for keyword in keywords:
            matches = search_manual_content(equipment_id, keyword)
            results.extend(matches)
        
        # Remove duplicates
        unique_results = []
        seen = set()
        for result in results:
            key = (result['section'], result['issue_type'])
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        return unique_results
    
    def get_parts_list(self, equipment_id, anomaly_type):
        """
        Get required parts for a specific issue
        
        Args:
            equipment_id: Equipment identifier
            anomaly_type: Type of anomaly
        
        Returns:
            list: Required parts with details
        """
        result = self.query_manual(equipment_id, anomaly_type)
        return result.get("required_parts", [])
    
    def get_resolution_steps(self, equipment_id, anomaly_type):
        """
        Get resolution steps for a specific issue
        
        Args:
            equipment_id: Equipment identifier
            anomaly_type: Type of anomaly
        
        Returns:
            list: Step-by-step resolution instructions
        """
        result = self.query_manual(equipment_id, anomaly_type)
        return result.get("resolution_steps", [])
    
    def format_for_llm(self, equipment_id, anomaly_type, sensor_data=None):
        """
        Format RAG results for LLM prompt
        
        Args:
            equipment_id: Equipment identifier
            anomaly_type: Type of anomaly
            sensor_data: Optional sensor readings
        
        Returns:
            str: Formatted context for LLM
        """
        result = self.query_manual(equipment_id, anomaly_type, sensor_data)
        
        context = f"""
EQUIPMENT INFORMATION:
- Equipment ID: {result['equipment_id']}
- Equipment Name: {result['equipment_name']}
- Equipment Type: {result['equipment_type']}

ANOMALY DETECTED:
- Type: {result['anomaly_type']}
- Symptoms: {result['troubleshooting']['symptoms']}

POSSIBLE CAUSES:
{self._format_list(result.get('possible_causes', []))}

DIAGNOSIS STEPS:
{self._format_list(result.get('diagnosis_steps', []))}

RESOLUTION STEPS:
{self._format_list(result.get('resolution_steps', []))}

REQUIRED PARTS:
{self._format_parts(result.get('required_parts', []))}

ESTIMATED REPAIR TIME: {result.get('estimated_time', 'Unknown')}

SAFETY PRECAUTIONS:
{self._format_list(result.get('safety_precautions', []))}
"""
        
        if sensor_data:
            context = f"CURRENT SENSOR READINGS:\n{result.get('sensor_context', '')}\n\n" + context
        
        return context.strip()
    
    def _format_list(self, items):
        """Format list items with bullets"""
        if not items:
            return "- None specified"
        return "\n".join([f"- {item}" for item in items])
    
    def _format_parts(self, parts):
        """Format parts list"""
        if not parts:
            return "- No parts required"
        
        formatted = []
        for part in parts:
            formatted.append(
                f"- {part['part_number']}: {part['description']} "
                f"(Cost: {part['cost']}, Qty: {part['quantity']})"
            )
        return "\n".join(formatted)


# Convenience function for quick queries
def query_equipment_manual(equipment_id, anomaly_type, sensor_data=None, use_pinecone=False):
    """
    Quick function to query equipment manual
    This is the main interface that Agent 2 will use
    
    Args:
        equipment_id: Equipment identifier
        anomaly_type: Type of anomaly detected
        sensor_data: Optional sensor readings
        use_pinecone: Use Pinecone vector database if available
    
    Returns:
        dict: RAG query results
    """
    rag = MockRAG(use_pinecone=use_pinecone)
    return rag.query_manual(equipment_id, anomaly_type, sensor_data)


# Quick test
if __name__ == "__main__":
    print("=== Testing Mock RAG System ===\n")
    
    rag = MockRAG()
    
    # Test 1: HVAC overheating
    print("Test 1: HVAC Overheating Query")
    print("-" * 50)
    result = rag.query_manual(
        "HVAC-001",
        "overheating",
        {"temp": 32.0, "pressure": 54.0, "current": 13.0}
    )
    print(f"Equipment: {result['equipment_name']}")
    print(f"Anomaly: {result['anomaly_type']}")
    print(f"Symptoms: {result['troubleshooting']['symptoms']}")
    print(f"\nRequired Parts ({len(result['required_parts'])}):")
    for part in result['required_parts']:
        print(f"  - {part['part_number']}: {part['description']} ({part['cost']})")
    print(f"\nEstimated Time: {result['estimated_time']}")
    print(f"Resolution Steps: {len(result['resolution_steps'])} steps")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Motor vibration
    print("Test 2: Motor Excessive Vibration Query")
    print("-" * 50)
    result = rag.query_manual(
        "MOTOR-001",
        "excessive_vibration",
        {"vibration": 4.5, "temp": 62.0, "current": 26.0}
    )
    print(f"Equipment: {result['equipment_name']}")
    print(f"Anomaly: {result['anomaly_type']}")
    print(f"Symptoms: {result['troubleshooting']['symptoms']}")
    print(f"\nRequired Parts ({len(result['required_parts'])}):")
    for part in result['required_parts']:
        print(f"  - {part['part_number']}: {part['description']} ({part['cost']})")
    print(f"\nEstimated Time: {result['estimated_time']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Format for LLM
    print("Test 3: LLM-Formatted Context")
    print("-" * 50)
    llm_context = rag.format_for_llm(
        "HVAC-001",
        "overheating",
        {"temp": 32.0, "pressure": 54.0}
    )
    print(llm_context[:500] + "...")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Convenience function
    print("Test 4: Convenience Function")
    print("-" * 50)
    result = query_equipment_manual("MOTOR-001", "high_current")
    print(f"Equipment: {result['equipment_id']}")
    print(f"Issue: {result['anomaly_type']}")
    print(f"Parts needed: {len(result['required_parts'])}")
    
    print("\n=== All Tests Passed ===")

# Made with Bob
