"""
Telemetry Anomaly Detection Tool for watsonx Orchestrate
Detects anomalies in IoT sensor data based on predefined thresholds
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any


@tool(
    name="detect_anomaly",
    display_name="Detect Sensor Anomaly",
    description="Analyzes IoT sensor data to detect anomalies based on equipment-specific thresholds. Returns anomaly type and severity if detected."
)
def detect_anomaly(equipment_id: str, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect anomalies in sensor data for equipment monitoring.
    
    Args:
        equipment_id (str): The unique identifier for the equipment (e.g., 'HVAC-001', 'MOTOR-001')
        sensor_data (dict): Dictionary containing sensor readings with keys like 'temperature', 'vibration', 'pressure'
    
    Returns:
        dict: Anomaly detection result containing:
            - anomaly_detected (bool): Whether an anomaly was found
            - anomaly_type (str): Type of anomaly if detected
            - severity (str): Severity level (normal, warning, critical)
            - equipment_id (str): Equipment identifier
            - sensor_data (dict): Original sensor readings
    """
    
    # Define thresholds for different equipment types
    thresholds = {
        'HVAC-001': {
            'temperature': {'warning': 75, 'critical': 85},
            'pressure': {'warning': 45, 'critical': 50}
        },
        'HVAC-002': {
            'temperature': {'warning': 75, 'critical': 85},
            'pressure': {'warning': 45, 'critical': 50}
        },
        'MOTOR-001': {
            'vibration': {'warning': 8, 'critical': 10},
            'temperature': {'warning': 80, 'critical': 90}
        },
        'MOTOR-002': {
            'vibration': {'warning': 8, 'critical': 10},
            'temperature': {'warning': 80, 'critical': 90}
        }
    }
    
    # Get thresholds for this equipment
    equipment_thresholds = thresholds.get(equipment_id, {})
    
    anomaly_detected = False
    anomaly_type = None
    severity = 'normal'
    
    # Check each sensor reading against thresholds
    for sensor_type, value in sensor_data.items():
        if sensor_type in equipment_thresholds:
            threshold = equipment_thresholds[sensor_type]
            
            if value >= threshold['critical']:
                anomaly_detected = True
                severity = 'critical'
                if sensor_type == 'temperature':
                    anomaly_type = 'overheating'
                elif sensor_type == 'vibration':
                    anomaly_type = 'excessive_vibration'
                elif sensor_type == 'pressure':
                    anomaly_type = 'pressure_spike'
                break
            elif value >= threshold['warning']:
                if severity != 'critical':
                    anomaly_detected = True
                    severity = 'warning'
                    if sensor_type == 'temperature':
                        anomaly_type = 'overheating'
                    elif sensor_type == 'vibration':
                        anomaly_type = 'excessive_vibration'
                    elif sensor_type == 'pressure':
                        anomaly_type = 'pressure_spike'
    
    return {
        'anomaly_detected': anomaly_detected,
        'anomaly_type': anomaly_type,
        'severity': severity,
        'equipment_id': equipment_id,
        'sensor_data': sensor_data
    }

# Made with Bob
