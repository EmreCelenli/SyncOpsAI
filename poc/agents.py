"""
All 3 agents for SyncOps AI POC
Simple implementations focused on demo impact
"""

import uuid
from poc.state import State
from poc.data import THRESHOLDS


# ============================================================================
# AGENT 1: TELEMETRY LISTENER - Anomaly Detection
# ============================================================================

def agent_1_detect(state: State) -> State:
    """
    Agent 1: Detect anomalies using simple threshold-based detection.
    
    For POC: Just check if sensor value exceeds hardcoded threshold.
    Production would use statistical methods (3-sigma, drift detection, etc.)
    """
    equipment_id = state["equipment_id"]
    sensor_value = state["sensor_value"]
    sensor_type = state["sensor_type"]
    
    # Get threshold for this equipment
    if equipment_id not in THRESHOLDS:
        return {
            **state,
            "anomaly": False,
            "anomaly_type": "none",
            "messages": [f"⚠️  Agent 1: Unknown equipment {equipment_id}"]
        }
    
    threshold = THRESHOLDS[equipment_id].get(sensor_type)
    if threshold is None:
        return {
            **state,
            "anomaly": False,
            "anomaly_type": "none",
            "messages": [f"⚠️  Agent 1: Unknown sensor type {sensor_type}"]
        }
    
    # Check for anomaly
    if sensor_value > threshold:
        # Determine anomaly type based on sensor
        if sensor_type == "temperature":
            anomaly_type = "overheating"
            emoji = "🔥"
        elif sensor_type == "vibration":
            anomaly_type = "vibration"
            emoji = "📳"
        else:
            anomaly_type = "spike"
            emoji = "⚡"
        
        return {
            **state,
            "anomaly": True,
            "anomaly_type": anomaly_type,
            "messages": [
                f"{emoji} Agent 1: ANOMALY DETECTED!",
                f"   Equipment: {equipment_id}",
                f"   {sensor_type.title()}: {sensor_value} (threshold: {threshold})",
                f"   Type: {anomaly_type}"
            ]
        }
    else:
        return {
            **state,
            "anomaly": False,
            "anomaly_type": "none",
            "messages": [
                f"✅ Agent 1: Normal operation",
                f"   Equipment: {equipment_id}",
                f"   {sensor_type.title()}: {sensor_value} (threshold: {threshold})"
            ]
        }


# ============================================================================
# AGENT 2: DIAGNOSTIC EXPERT - Root Cause Analysis
# ============================================================================

def agent_2_diagnose(state: State) -> State:
    """
    Agent 2: Diagnose the issue using RAG + LLM.
    
    Now integrated with Developer A's real RAG and diagnosis functions!
    """
    if not state["anomaly"]:
        return {
            **state,
            "messages": state["messages"] + ["ℹ️  Agent 2: No anomaly to diagnose"]
        }
    
    equipment_id = state["equipment_id"]
    anomaly_type = state["anomaly_type"]
    sensor_data = state["sensor_data"]
    
    # Use Developer A's real functions (with fallback to mock)
    if DEVELOPER_A_INTEGRATED:
        # Real RAG query
        rag_results = query_manual_real(equipment_id, anomaly_type, sensor_data)
        
        # Real LLM diagnosis
        diagnosis_result = diagnose_real(equipment_id, anomaly_type, sensor_data, rag_results)
        
        # Extract information from Developer A's format
        root_cause = diagnosis_result.get("root_cause", "Unknown issue")
        parts_needed = []
        for part in diagnosis_result.get("required_parts", []):
            part_str = f"{part['part_number']}: {part['description']} ({part['cost']})"
            parts_needed.append(part_str)
        estimated_time = diagnosis_result.get("estimated_time", "Unknown")
        
    else:
        # Fallback to mock functions
        manual_info = query_manual_mock(equipment_id, anomaly_type)
        diagnosis_result = diagnose_mock(equipment_id, anomaly_type, manual_info)
        root_cause = diagnosis_result["root_cause"]
        parts_needed = diagnosis_result["parts"]
        estimated_time = diagnosis_result["time"]
    
    return {
        **state,
        "diagnosis": root_cause,
        "parts_needed": parts_needed,
        "estimated_time": estimated_time,
        "messages": state["messages"] + [
            f"🔍 Agent 2: Diagnosis complete",
            f"   Root Cause: {root_cause}",
            f"   Parts Needed: {', '.join(parts_needed) if parts_needed else 'None'}",
            f"   Estimated Time: {estimated_time}"
        ]
    }


# Import Developer A's functions
import sys
import os
from typing import Optional, Callable, Any

# Add parent directory to path to import Developer A's modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize as None, will be set if imports succeed
query_equipment_manual: Optional[Callable] = None
diagnose_equipment_issue: Optional[Callable] = None
DEVELOPER_A_INTEGRATED = False

try:
    from rag import query_equipment_manual  # type: ignore
    from diagnosis import diagnose as diagnose_equipment_issue  # type: ignore
    DEVELOPER_A_INTEGRATED = True
except ImportError:
    print("⚠️  Developer A's modules not found. Using mock functions.")


def query_manual_real(equipment_id: str, anomaly_type: str, sensor_data: dict) -> dict:
    """
    Real RAG query using Developer A's implementation.
    """
    if DEVELOPER_A_INTEGRATED and query_equipment_manual is not None:
        return query_equipment_manual(equipment_id, anomaly_type, sensor_data)
    else:
        # Fallback to mock
        return query_manual_mock(equipment_id, anomaly_type)


def diagnose_real(equipment_id: str, anomaly_type: str, sensor_data: dict, rag_results: dict) -> dict:
    """
    Real diagnosis using Developer A's implementation.
    """
    if DEVELOPER_A_INTEGRATED and diagnose_equipment_issue is not None:
        # Developer A's diagnose function expects just equipment_id, anomaly_type, and sensor_data
        return diagnose_equipment_issue(equipment_id, anomaly_type, sensor_data, use_ai=False)
    else:
        # Fallback to mock
        return diagnose_mock(equipment_id, anomaly_type, {})


def query_manual_mock(equipment_id: str, anomaly_type: str) -> dict:
    """Mock RAG query function (fallback)."""
    if "HVAC" in equipment_id:
        return {
            "troubleshooting": "High temperature indicates clogged air filter",
            "parts": ["Air Filter AF-2024"],
            "steps": ["Shut down system", "Replace filter", "Test operation"]
        }
    elif "MOTOR" in equipment_id:
        return {
            "troubleshooting": "Excessive vibration indicates worn bearings",
            "parts": ["Bearing RB-500"],
            "steps": ["Stop conveyor", "Replace bearings", "Lubricate", "Test"]
        }
    else:
        return {
            "troubleshooting": "Unknown issue",
            "parts": [],
            "steps": []
        }


def diagnose_mock(equipment_id: str, anomaly_type: str, manual_info: dict) -> dict:
    """Mock LLM diagnosis function (fallback)."""
    if "HVAC" in equipment_id:
        return {
            "root_cause": "Clogged air filter causing overheating",
            "parts": ["Air Filter AF-2024 ($45)"],
            "time": "30 minutes"
        }
    elif "MOTOR" in equipment_id:
        return {
            "root_cause": "Worn bearings causing excessive vibration",
            "parts": ["Bearing RB-500 ($120)"],
            "time": "2 hours"
        }
    else:
        return {
            "root_cause": "Unknown issue",
            "parts": [],
            "time": "Unknown"
        }


# ============================================================================
# AGENT 3: ORCHESTRATOR - Work Order & Inventory
# ============================================================================

def agent_3_action(state: State) -> State:
    """
    Agent 3: Create work order and check inventory using watsonx Orchestrate.
    
    For POC: Use mock watsonx Orchestrate calls.
    Production would use real watsonx Orchestrate API.
    """
    if not state["diagnosis"]:
        return {
            **state,
            "messages": state["messages"] + ["ℹ️  Agent 3: No diagnosis to act on"]
        }
    
    equipment_id = state["equipment_id"]
    diagnosis = state["diagnosis"]
    parts_needed = state["parts_needed"]
    
    # Mock work order creation (watsonx Orchestrate skill)
    work_order_id = create_work_order_mock(equipment_id, diagnosis, parts_needed)
    
    # Mock inventory check (watsonx Orchestrate skill)
    parts_available = check_inventory_mock(parts_needed)
    
    return {
        **state,
        "work_order_id": work_order_id,
        "parts_available": parts_available,
        "messages": state["messages"] + [
            f"📋 Agent 3: Work order created",
            f"   Work Order ID: {work_order_id}",
            f"   Parts Status: {'✅ All in stock' if parts_available else '⚠️  Some on backorder'}",
            f"   Next: Assign to technician"
        ]
    }


def create_work_order_mock(equipment_id: str, diagnosis: str, parts: list[str]) -> str:
    """
    Mock watsonx Orchestrate "Create Work Order" skill.
    
    Production would call real watsonx Orchestrate API.
    """
    # Generate unique work order ID
    work_order_id = f"WO-{uuid.uuid4().hex[:6].upper()}"
    return work_order_id


def check_inventory_mock(parts: list[str]) -> bool:
    """
    Mock watsonx Orchestrate "Check Inventory" skill.
    
    Production would call real watsonx Orchestrate API.
    """
    # For demo, always return True (parts available)
    # In real system, would query inventory database
    return True


# ============================================================================
# INTEGRATION INTERFACE FOR DEVELOPER A
# ============================================================================

def integrate_developer_a_functions(query_manual_func, diagnose_func):
    """
    Replace mock functions with Developer A's real implementations.
    
    Call this on Day 2 morning after receiving Developer A's functions:
    
    from developer_a_functions import query_manual, diagnose
    integrate_developer_a_functions(query_manual, diagnose)
    """
    global query_manual_mock, diagnose_mock
    query_manual_mock = query_manual_func
    diagnose_mock = diagnose_func
    print("✅ Developer A's functions integrated successfully!")

# Made with Bob
