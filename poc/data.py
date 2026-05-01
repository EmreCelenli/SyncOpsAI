"""
Hardcoded test data for POC demo scenarios
"""

DEMO_SCENARIOS = [
    {
        "name": "HVAC Overheating",
        "equipment_id": "HVAC-001",
        "sensor_value": 32.0,
        "sensor_type": "temperature",
        "expected_anomaly": "overheating",
        "expected_diagnosis": "Clogged air filter"
    },
    {
        "name": "Motor Vibration",
        "equipment_id": "MOTOR-001",
        "sensor_value": 4.2,
        "sensor_type": "vibration",
        "expected_anomaly": "vibration",
        "expected_diagnosis": "Worn bearings"
    }
]

# Equipment-specific thresholds for anomaly detection
THRESHOLDS = {
    "HVAC-001": {
        "temperature": 28.0  # Celsius
    },
    "MOTOR-001": {
        "vibration": 3.0  # Hz
    }
}

# Made with Bob
