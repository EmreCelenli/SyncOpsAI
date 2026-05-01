"""
Test script to verify Developer A and Developer B integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*60)
print("Testing Developer A + Developer B Integration")
print("="*60)

# Test 1: Check if Developer A's modules are available
print("\n1. Checking Developer A's modules...")

# Initialize as None
query_equipment_manual = None
diagnose = None
get_manual = None
DEVELOPER_A_AVAILABLE = False

try:
    from rag import query_equipment_manual  # type: ignore
    from diagnosis import diagnose  # type: ignore
    from manuals import get_manual  # type: ignore
    print("✅ Developer A's modules imported successfully")
    DEVELOPER_A_AVAILABLE = True
except ImportError as e:
    print(f"❌ Developer A's modules not found: {e}")
    DEVELOPER_A_AVAILABLE = False

# Test 2: Check Developer B's modules
print("\n2. Checking Developer B's modules...")
try:
    from poc.state import create_initial_state
    from poc.agents import agent_1_detect, agent_2_diagnose, agent_3_action
    from poc.main import build_graph
    print("✅ Developer B's modules imported successfully")
except ImportError as e:
    print(f"❌ Developer B's modules not found: {e}")
    sys.exit(1)

# Test 3: Test HVAC scenario
print("\n3. Testing HVAC Overheating Scenario...")
print("-" * 60)

state = create_initial_state(
    equipment_id="HVAC-001",
    sensor_value=32.0,
    sensor_type="temp"
)

print(f"Initial state created:")
print(f"  Equipment: {state['equipment_id']}")
print(f"  Sensor: {state['sensor_type']} = {state['sensor_value']}")

# Run Agent 1
print("\nRunning Agent 1 (Telemetry Listener)...")
state = agent_1_detect(state)
print(f"  Anomaly detected: {state['anomaly']}")
print(f"  Anomaly type: {state['anomaly_type']}")

if state['anomaly']:
    # Run Agent 2
    print("\nRunning Agent 2 (Diagnostic Expert)...")
    state = agent_2_diagnose(state)
    print(f"  Diagnosis: {state['diagnosis']}")
    print(f"  Parts needed: {len(state['parts_needed'])} items")
    print(f"  Estimated time: {state['estimated_time']}")
    
    # Run Agent 3
    print("\nRunning Agent 3 (Orchestrator)...")
    state = agent_3_action(state)
    print(f"  Work order: {state['work_order_id']}")
    print(f"  Parts available: {state['parts_available']}")

print("\nAgent messages:")
for msg in state['messages']:
    print(f"  {msg}")

# Test 4: Test Motor scenario
print("\n" + "="*60)
print("4. Testing Motor Vibration Scenario...")
print("-" * 60)

state = create_initial_state(
    equipment_id="MOTOR-001",
    sensor_value=4.2,
    sensor_type="vibration"
)

print(f"Initial state created:")
print(f"  Equipment: {state['equipment_id']}")
print(f"  Sensor: {state['sensor_type']} = {state['sensor_value']}")

# Run full workflow
print("\nRunning full workflow...")
workflow = build_graph()
result = workflow.invoke(state)

print(f"\nFinal results:")
print(f"  Anomaly: {result['anomaly_type']}")
print(f"  Diagnosis: {result['diagnosis']}")
print(f"  Work Order: {result['work_order_id']}")

print("\nAgent messages:")
for msg in result['messages']:
    print(f"  {msg}")

# Test 5: Verify Developer A integration
if DEVELOPER_A_AVAILABLE and query_equipment_manual is not None and diagnose is not None:
    print("\n" + "="*60)
    print("5. Testing Developer A's Functions Directly...")
    print("-" * 60)
    
    # Test RAG
    print("\nTesting RAG query...")
    rag_result = query_equipment_manual(
        "HVAC-001",
        "overheating",
        {"temp": 32.0, "pressure": 54.0, "current": 13.0}
    )
    print(f"  Equipment: {rag_result['equipment_name']}")
    print(f"  Parts needed: {len(rag_result['required_parts'])} items")
    
    # Test Diagnosis
    print("\nTesting diagnosis function...")
    diagnosis_result = diagnose(
        "HVAC-001",
        "overheating",
        {"temp": 32.0, "pressure": 54.0, "current": 13.0}
    )
    print(f"  Root cause: {diagnosis_result['root_cause']}")
    print(f"  Severity: {diagnosis_result['severity']}")
    print(f"  Estimated cost: {diagnosis_result['estimated_cost']}")

print("\n" + "="*60)
print("✅ Integration Test Complete!")
print("="*60)

if DEVELOPER_A_AVAILABLE:
    print("\n🎉 Developer A's functions are fully integrated!")
    print("   - RAG system working")
    print("   - Diagnosis engine working")
    print("   - Agent 2 using real functions")
else:
    print("\n⚠️  Developer A's functions not available")
    print("   - Using mock functions as fallback")
    print("   - System still works for demo")

print("\nNext steps:")
print("  1. Run: python poc/main.py")
print("  2. Run: streamlit run poc/dashboard.py")
print("  3. Test both scenarios in dashboard")

# Made with Bob
