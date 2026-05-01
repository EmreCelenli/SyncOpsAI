"""
Equipment Diagnosis Tool for watsonx Orchestrate
Generates diagnostic reports using RAG and AI-powered analysis
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, List


@tool(
    name="generate_diagnosis",
    display_name="Generate Equipment Diagnosis",
    description="Analyzes equipment anomalies and generates comprehensive diagnostic reports with root cause analysis, resolution steps, and required parts using RAG and AI."
)
def generate_diagnosis(
    equipment_id: str,
    anomaly_type: str,
    sensor_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate diagnostic report for equipment anomaly.
    
    Args:
        equipment_id (str): The unique identifier for the equipment (e.g., 'HVAC-001', 'MOTOR-001')
        anomaly_type (str): Type of detected anomaly (e.g., 'overheating', 'excessive_vibration')
        sensor_data (dict): Dictionary containing current sensor readings
    
    Returns:
        dict: Diagnostic report containing:
            - equipment_id (str): Equipment identifier
            - anomaly_type (str): Type of anomaly
            - root_cause (str): Identified root cause
            - severity (str): Severity level
            - resolution_steps (list): Step-by-step resolution instructions
            - required_parts (list): Parts needed for repair
            - estimated_cost (str): Total estimated repair cost
            - manual_reference (str): Reference to equipment manual section
    """
    
    # Template-based diagnosis (simplified for POC)
    diagnosis_templates = {
        'HVAC-001': {
            'overheating': {
                'root_cause': 'Clogged air filter restricting airflow',
                'severity': 'medium',
                'resolution_steps': [
                    'Turn off HVAC system',
                    'Remove and inspect air filter',
                    'Replace filter if clogged',
                    'Check refrigerant levels',
                    'Restart system and monitor temperature'
                ],
                'required_parts': [
                    {'part_number': 'FILTER-001', 'name': 'Air Filter', 'quantity': 1, 'cost': '$45'}
                ],
                'manual_reference': 'Section 4.2: Air Filter Maintenance'
            }
        },
        'MOTOR-001': {
            'excessive_vibration': {
                'root_cause': 'Worn motor bearings causing imbalance',
                'severity': 'high',
                'resolution_steps': [
                    'Stop motor immediately',
                    'Inspect bearings for wear',
                    'Replace worn bearings',
                    'Realign motor shaft',
                    'Test run and verify vibration levels'
                ],
                'required_parts': [
                    {'part_number': 'BEARING-001', 'name': 'Motor Bearing', 'quantity': 2, 'cost': '$120'}
                ],
                'manual_reference': 'Section 3.1: Bearing Replacement'
            }
        }
    }
    
    # Get diagnosis template
    equipment_diagnoses = diagnosis_templates.get(equipment_id, {})
    diagnosis = equipment_diagnoses.get(anomaly_type, {
        'root_cause': 'Unknown issue - manual inspection required',
        'severity': 'medium',
        'resolution_steps': ['Contact maintenance team for inspection'],
        'required_parts': [],
        'manual_reference': 'General Troubleshooting'
    })
    
    # Calculate total cost
    total_cost = 0
    for part in diagnosis.get('required_parts', []):
        cost_str = part['cost'].replace('$', '')
        total_cost += float(cost_str) * part['quantity']
    
    return {
        'equipment_id': equipment_id,
        'anomaly_type': anomaly_type,
        'root_cause': diagnosis['root_cause'],
        'severity': diagnosis['severity'],
        'resolution_steps': diagnosis['resolution_steps'],
        'required_parts': diagnosis.get('required_parts', []),
        'estimated_cost': f'${total_cost:.2f}',
        'manual_reference': diagnosis['manual_reference'],
        'sensor_data': sensor_data
    }

# Made with Bob
