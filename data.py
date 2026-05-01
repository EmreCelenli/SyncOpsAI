"""
Hardcoded sensor data scenarios for POC demo
Task 1: 30 minutes - Simple, hardcoded data for 2 demo scenarios
"""

from datetime import datetime, timedelta

# Demo scenarios with hardcoded sensor readings
DEMO_SCENARIOS = {
    "hvac_overheating": {
        "equipment_id": "HVAC-001",
        "equipment_type": "HVAC",
        "description": "HVAC system overheating scenario",
        "readings": [
            {"temp": 22.0, "pressure": 50.0, "current": 10.0, "time": "10:00:00", "status": "normal"},
            {"temp": 23.5, "pressure": 51.0, "current": 10.2, "time": "10:01:00", "status": "normal"},
            {"temp": 25.0, "pressure": 52.0, "current": 10.5, "time": "10:02:00", "status": "normal"},
            {"temp": 26.5, "pressure": 52.5, "current": 11.0, "time": "10:03:00", "status": "warning"},
            {"temp": 28.5, "pressure": 53.0, "current": 11.5, "time": "10:04:00", "status": "warning"},
            {"temp": 30.0, "pressure": 53.5, "current": 12.5, "time": "10:05:00", "status": "anomaly"},
            {"temp": 32.0, "pressure": 54.0, "current": 13.0, "time": "10:06:00", "status": "critical"},
        ],
        "anomaly_threshold": {"temp": 28.0, "pressure": 60.0, "current": 15.0},
        "anomaly_detected_at": 5,  # Index where anomaly starts
        "expected_diagnosis": "Clogged air filter causing overheating"
    },
    
    "motor_vibration": {
        "equipment_id": "MOTOR-001",
        "equipment_type": "Conveyor Motor",
        "description": "Conveyor motor excessive vibration scenario",
        "readings": [
            {"vibration": 1.2, "temp": 45.0, "current": 18.0, "time": "10:00:00", "status": "normal"},
            {"vibration": 1.5, "temp": 46.0, "current": 18.5, "time": "10:01:00", "status": "normal"},
            {"vibration": 1.8, "temp": 48.0, "current": 19.0, "time": "10:02:00", "status": "normal"},
            {"vibration": 2.5, "temp": 52.0, "current": 20.0, "time": "10:03:00", "status": "warning"},
            {"vibration": 3.2, "temp": 55.0, "current": 22.0, "time": "10:04:00", "status": "warning"},
            {"vibration": 4.0, "temp": 58.0, "current": 24.0, "time": "10:05:00", "status": "anomaly"},
            {"vibration": 4.5, "temp": 62.0, "current": 26.0, "time": "10:06:00", "status": "critical"},
        ],
        "anomaly_threshold": {"vibration": 3.5, "temp": 75.0, "current": 30.0},
        "anomaly_detected_at": 5,  # Index where anomaly starts
        "expected_diagnosis": "Worn bearings causing excessive vibration"
    }
}


def get_scenario(scenario_name):
    """
    Get a demo scenario by name
    
    Args:
        scenario_name: 'hvac_overheating' or 'motor_vibration'
    
    Returns:
        dict: Scenario data with readings
    """
    if scenario_name not in DEMO_SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_name}. Available: {list(DEMO_SCENARIOS.keys())}")
    
    return DEMO_SCENARIOS[scenario_name]


def get_latest_reading(scenario_name):
    """
    Get the most recent (critical) reading from a scenario
    
    Args:
        scenario_name: 'hvac_overheating' or 'motor_vibration'
    
    Returns:
        dict: Latest sensor reading
    """
    scenario = get_scenario(scenario_name)
    return scenario["readings"][-1]


def get_reading_at_index(scenario_name, index):
    """
    Get a specific reading from a scenario
    
    Args:
        scenario_name: Scenario name
        index: Reading index (0-based)
    
    Returns:
        dict: Sensor reading at index
    """
    scenario = get_scenario(scenario_name)
    if index >= len(scenario["readings"]):
        return scenario["readings"][-1]
    return scenario["readings"][index]


def simulate_sensor_stream(scenario_name):
    """
    Generator that yields sensor readings one by one (for demo animation)
    
    Args:
        scenario_name: Scenario to simulate
    
    Yields:
        dict: Sensor reading with equipment info
    """
    scenario = get_scenario(scenario_name)
    
    for reading in scenario["readings"]:
        yield {
            "equipment_id": scenario["equipment_id"],
            "equipment_type": scenario["equipment_type"],
            "reading": reading,
            "timestamp": datetime.now().isoformat()
        }


def check_anomaly(scenario_name, reading):
    """
    Simple threshold-based anomaly detection
    
    Args:
        scenario_name: Scenario name
        reading: Sensor reading dict
    
    Returns:
        tuple: (is_anomaly, anomaly_type, severity)
    """
    scenario = get_scenario(scenario_name)
    thresholds = scenario["anomaly_threshold"]
    
    # Check each sensor against threshold
    anomalies = []
    
    if scenario_name == "hvac_overheating":
        if reading.get("temp", 0) > thresholds["temp"]:
            anomalies.append(("overheating", "critical" if reading["temp"] > 30 else "warning"))
        if reading.get("pressure", 0) < 35:  # Low pressure
            anomalies.append(("low_pressure", "warning"))
        if reading.get("current", 0) > thresholds["current"]:
            anomalies.append(("high_current", "warning"))
    
    elif scenario_name == "motor_vibration":
        if reading.get("vibration", 0) > thresholds["vibration"]:
            anomalies.append(("excessive_vibration", "critical" if reading["vibration"] > 4.0 else "warning"))
        if reading.get("temp", 0) > thresholds["temp"]:
            anomalies.append(("overheating", "warning"))
        if reading.get("current", 0) > thresholds["current"]:
            anomalies.append(("high_current", "warning"))
    
    if anomalies:
        # Return the most severe anomaly
        anomaly_type, severity = anomalies[0]
        return True, anomaly_type, severity
    
    return False, None, None


# Quick test
if __name__ == "__main__":
    print("=== Testing Demo Scenarios ===\n")
    
    # Test HVAC scenario
    print("HVAC Overheating Scenario:")
    hvac = get_scenario("hvac_overheating")
    print(f"Equipment: {hvac['equipment_id']}")
    print(f"Total readings: {len(hvac['readings'])}")
    
    latest = get_latest_reading("hvac_overheating")
    print(f"Latest reading: {latest}")
    
    is_anomaly, anomaly_type, severity = check_anomaly("hvac_overheating", latest)
    print(f"Anomaly detected: {is_anomaly}, Type: {anomaly_type}, Severity: {severity}")
    
    print("\n" + "="*50 + "\n")
    
    # Test Motor scenario
    print("Motor Vibration Scenario:")
    motor = get_scenario("motor_vibration")
    print(f"Equipment: {motor['equipment_id']}")
    print(f"Total readings: {len(motor['readings'])}")
    
    latest = get_latest_reading("motor_vibration")
    print(f"Latest reading: {latest}")
    
    is_anomaly, anomaly_type, severity = check_anomaly("motor_vibration", latest)
    print(f"Anomaly detected: {is_anomaly}, Type: {anomaly_type}, Severity: {severity}")
    
    print("\n" + "="*50 + "\n")
    
    # Test streaming
    print("Simulating sensor stream (first 3 readings):")
    for i, data in enumerate(simulate_sensor_stream("hvac_overheating")):
        if i >= 3:
            break
        print(f"  {data['reading']['time']}: {data['reading']}")

# Made with Bob
