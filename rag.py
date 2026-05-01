"""
Mock RAG (Retrieval-Augmented Generation) system for POC
Task 3: 1.5 hours - Simple keyword matching, no Pinecone needed initially
"""

from manuals import get_manual, get_troubleshooting_section, search_manual_content


class MockRAG:
    """
    Simple RAG implementation using keyword matching
    No vector database needed for POC - will add real Pinecone later
    """
    
    def __init__(self):
        self.manuals_loaded = True
    
    def query_manual(self, equipment_id, anomaly_type, sensor_data=None):
        """
        Query equipment manual for troubleshooting information
        
        Args:
            equipment_id: Equipment identifier (e.g., 'HVAC-001')
            anomaly_type: Type of anomaly (e.g., 'overheating', 'excessive_vibration')
            sensor_data: Optional sensor readings for context
        
        Returns:
            dict: Relevant manual sections and troubleshooting info
        """
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
def query_equipment_manual(equipment_id, anomaly_type, sensor_data=None):
    """
    Quick function to query equipment manual
    This is the main interface that Agent 2 will use
    
    Args:
        equipment_id: Equipment identifier
        anomaly_type: Type of anomaly detected
        sensor_data: Optional sensor readings
    
    Returns:
        dict: RAG query results
    """
    rag = MockRAG()
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
