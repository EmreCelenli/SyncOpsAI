"""
State Schema for SyncOps AI POC
Simple state dictionary for agent communication
"""

from typing import TypedDict, Optional


class State(TypedDict):
    """
    Shared state passed between all agents.
    Keep it simple for POC - only essential fields.
    """
    # Input
    equipment_id: str
    sensor_value: float
    sensor_type: str  # "temperature", "vibration", etc.
    sensor_data: dict  # Full sensor readings for Developer A's functions
    
    # Agent 1 output
    anomaly: bool
    anomaly_type: str  # "overheating", "vibration", "none"
    
    # Agent 2 output
    diagnosis: str
    parts_needed: list[str]
    estimated_time: str
    
    # Agent 3 output
    work_order_id: str
    parts_available: bool
    
    # For dashboard display
    messages: list[str]


def create_initial_state(equipment_id: str, sensor_value: float, sensor_type: str) -> State:
    """
    Create initial state for workflow execution.
    
    Args:
        equipment_id: Equipment identifier (e.g., "HVAC-001")
        sensor_value: Current sensor reading
        sensor_type: Type of sensor ("temperature", "vibration", etc.)
    
    Returns:
        Initialized State ready for workflow
    """
    # Build sensor_data dict for Developer A's functions
    sensor_data = {sensor_type: sensor_value}
    
    return {
        "equipment_id": equipment_id,
        "sensor_value": sensor_value,
        "sensor_type": sensor_type,
        "sensor_data": sensor_data,
        "anomaly": False,
        "anomaly_type": "none",
        "diagnosis": "",
        "parts_needed": [],
        "estimated_time": "",
        "work_order_id": "",
        "parts_available": False,
        "messages": []
    }

# Made with Bob
