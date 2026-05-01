"""
Integration interface for Developer A's functions
This file documents the handoff between Developer A and Developer B
"""

# ============================================================================
# DEVELOPER A INTEGRATION INTERFACE
# ============================================================================

"""
Developer A: Provide these 2 functions by end of Day 1

These functions will be called by Agent 2 (Diagnostic Expert) to:
1. Query equipment manuals using RAG
2. Generate diagnosis using LLM

You can implement these with:
- Real Pinecone + Granite-Embedding (preferred)
- Mock implementations with hardcoded responses (acceptable for POC)
- Template-based responses (acceptable for POC)
"""


def query_manual(equipment_id: str, anomaly_type: str) -> dict:
    """
    Query equipment manual using RAG system.
    
    Args:
        equipment_id: Equipment identifier (e.g., "HVAC-001", "MOTOR-001")
        anomaly_type: Type of anomaly detected ("overheating", "vibration", etc.)
    
    Returns:
        {
            "troubleshooting": str,  # Relevant troubleshooting section
            "parts": list[str],      # List of part names/IDs
            "steps": list[str]       # Resolution steps
        }
    
    Example:
        >>> query_manual("HVAC-001", "overheating")
        {
            "troubleshooting": "High temperature indicates clogged air filter...",
            "parts": ["Air Filter AF-2024"],
            "steps": ["Shut down system", "Replace filter", "Test operation"]
        }
    
    Implementation Options:
    1. Real RAG: Use Pinecone + Granite-Embedding to query manual embeddings
    2. Mock: Return hardcoded responses based on equipment_id
    3. Template: Use simple if/else logic with predefined responses
    """
    raise NotImplementedError("Developer A: Implement this function")


def diagnose(equipment_id: str, anomaly_type: str, manual_content: dict) -> dict:
    """
    Generate diagnosis using LLM with RAG context.
    
    Args:
        equipment_id: Equipment identifier
        anomaly_type: Type of anomaly detected
        manual_content: Output from query_manual() function
    
    Returns:
        {
            "root_cause": str,       # Diagnosed root cause
            "parts": list[str],      # Parts needed with prices
            "time": str              # Estimated repair time
        }
    
    Example:
        >>> diagnose("HVAC-001", "overheating", manual_content)
        {
            "root_cause": "Clogged air filter causing overheating",
            "parts": ["Air Filter AF-2024 ($45)"],
            "time": "30 minutes"
        }
    
    Implementation Options:
    1. Real LLM: Use Granite-Vision-4.1-4B via watsonx.ai
    2. Template: Use f-strings to format manual_content into diagnosis
    3. Mock: Return hardcoded responses based on equipment_id
    """
    raise NotImplementedError("Developer A: Implement this function")


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================

"""
HOW TO INTEGRATE (Day 2 Morning):

1. Developer A creates file: developer_a_functions.py
   - Implements query_manual()
   - Implements diagnose()

2. Developer B updates agents.py:
   
   # At top of agents.py, replace mock imports:
   from developer_a_functions import query_manual, diagnose
   
   # In agent_2_diagnose(), replace:
   manual_info = query_manual_mock(equipment_id, anomaly_type)
   diagnosis_result = diagnose_mock(equipment_id, anomaly_type, manual_info)
   
   # With:
   manual_info = query_manual(equipment_id, anomaly_type)
   diagnosis_result = diagnose(equipment_id, anomaly_type, manual_info)

3. Test together:
   cd poc
   python main.py
   
   Should see real RAG/LLM results instead of mock responses.

TESTING CHECKLIST:
- [ ] query_manual() returns valid dict with all required keys
- [ ] diagnose() returns valid dict with all required keys
- [ ] Both functions handle HVAC-001 scenario
- [ ] Both functions handle MOTOR-001 scenario
- [ ] No exceptions thrown during execution
- [ ] Results display correctly in dashboard
"""


# ============================================================================
# TEST CASES FOR DEVELOPER A
# ============================================================================

def test_developer_a_functions():
    """
    Test cases for Developer A's functions.
    Run this to verify your implementations work correctly.
    """
    print("Testing Developer A's functions...")
    
    # Test Case 1: HVAC Overheating
    print("\n--- Test Case 1: HVAC Overheating ---")
    try:
        manual = query_manual("HVAC-001", "overheating")
        print(f"✅ query_manual returned: {manual}")
        
        diagnosis = diagnose("HVAC-001", "overheating", manual)
        print(f"✅ diagnose returned: {diagnosis}")
    except NotImplementedError:
        print("⚠️  Functions not implemented yet")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Case 2: Motor Vibration
    print("\n--- Test Case 2: Motor Vibration ---")
    try:
        manual = query_manual("MOTOR-001", "vibration")
        print(f"✅ query_manual returned: {manual}")
        
        diagnosis = diagnose("MOTOR-001", "vibration", manual)
        print(f"✅ diagnose returned: {diagnosis}")
    except NotImplementedError:
        print("⚠️  Functions not implemented yet")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("If you see ✅ for all tests, you're ready to integrate!")
    print("="*60)


if __name__ == "__main__":
    test_developer_a_functions()

# Made with Bob
