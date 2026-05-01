"""
Work Order Creation Tool for watsonx Orchestrate
Creates maintenance work orders based on diagnostic reports
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, List
from datetime import datetime


@tool(
    name="create_work_order",
    display_name="Create Maintenance Work Order",
    description="Creates a maintenance work order in the system based on diagnostic report. Assigns priority, schedules maintenance, and tracks required parts."
)
def create_work_order(
    equipment_id: str,
    root_cause: str,
    severity: str,
    resolution_steps: List[str],
    required_parts: List[Dict[str, Any]],
    estimated_cost: str
) -> Dict[str, Any]:
    """
    Create a maintenance work order for equipment repair.
    
    Args:
        equipment_id (str): The unique identifier for the equipment
        root_cause (str): Identified root cause of the issue
        severity (str): Severity level (low, medium, high, critical)
        resolution_steps (list): List of steps to resolve the issue
        required_parts (list): List of parts needed with part numbers and quantities
        estimated_cost (str): Total estimated cost for repair
    
    Returns:
        dict: Work order details containing:
            - work_order_id (str): Unique work order identifier
            - equipment_id (str): Equipment identifier
            - status (str): Current status of work order
            - priority (str): Priority level
            - created_at (str): Creation timestamp
            - estimated_completion (str): Estimated completion time
            - assigned_to (str): Assigned technician
            - parts_ordered (bool): Whether parts have been ordered
    """
    
    # Generate work order ID (in real system, this would be from database)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    work_order_id = f'WO-{timestamp}'
    
    # Map severity to priority
    priority_map = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'critical': 'Critical'
    }
    priority = priority_map.get(severity.lower(), 'Medium')
    
    # Estimate completion time based on severity
    completion_hours = {
        'low': 48,
        'medium': 24,
        'high': 8,
        'critical': 4
    }
    hours = completion_hours.get(severity.lower(), 24)
    
    # Assign technician based on equipment type
    if 'HVAC' in equipment_id:
        assigned_to = 'HVAC Specialist Team'
    elif 'MOTOR' in equipment_id:
        assigned_to = 'Motor Maintenance Team'
    else:
        assigned_to = 'General Maintenance Team'
    
    return {
        'work_order_id': work_order_id,
        'equipment_id': equipment_id,
        'status': 'Open',
        'priority': priority,
        'root_cause': root_cause,
        'resolution_steps': resolution_steps,
        'required_parts': required_parts,
        'estimated_cost': estimated_cost,
        'created_at': datetime.now().isoformat(),
        'estimated_completion_hours': hours,
        'assigned_to': assigned_to,
        'parts_ordered': len(required_parts) > 0
    }

# Made with Bob
