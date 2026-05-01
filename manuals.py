"""
Equipment manual content (fake/simplified for POC)
Task 2: 1 hour - Skip PDF generation, use structured text
"""

# Equipment manuals as structured text (no PDF needed for POC)
MANUAL_CONTENT = {
    "HVAC-001": {
        "equipment_name": "Industrial HVAC System Model HV-2000",
        "equipment_type": "HVAC",
        "manufacturer": "CoolAir Industries",
        "model": "HV-2000",
        "installation_date": "2023-01-15",
        
        "specifications": {
            "cooling_capacity": "50 tons",
            "operating_temp_range": "18-24°C",
            "operating_pressure_range": "45-55 PSI",
            "power_consumption": "8-12 Amps",
            "refrigerant_type": "R-410A"
        },
        
        "normal_parameters": """
        NORMAL OPERATING PARAMETERS:
        - Temperature: 18-24°C (optimal: 20-22°C)
        - Pressure: 45-55 PSI (optimal: 50 PSI)
        - Current Draw: 8-12 Amps (optimal: 10 Amps)
        - Humidity: 40-60%
        """,
        
        "troubleshooting": {
            "overheating": {
                "symptoms": "Temperature reading above 28°C, reduced cooling efficiency",
                "possible_causes": [
                    "Clogged air filter restricting airflow",
                    "Refrigerant leak or low refrigerant levels",
                    "Compressor malfunction",
                    "Condenser coil blockage",
                    "Faulty temperature sensor"
                ],
                "diagnosis_steps": [
                    "Check air filter condition - replace if dirty or clogged",
                    "Inspect refrigerant lines for leaks or damage",
                    "Test compressor operation and pressure readings",
                    "Clean condenser coils if blocked",
                    "Verify temperature sensor calibration"
                ],
                "resolution": [
                    "Turn off HVAC system immediately",
                    "Remove and inspect air filter",
                    "Replace air filter if clogged (Part: AF-2024)",
                    "Check refrigerant levels - refill if low",
                    "Clean condenser coils with approved cleaner",
                    "Restart system and monitor temperature for 30 minutes"
                ],
                "required_parts": [
                    {"part_number": "AF-2024", "description": "High-efficiency air filter", "cost": "$45", "quantity": 1},
                    {"part_number": "R410A-5LB", "description": "R-410A Refrigerant (5 lb)", "cost": "$120", "quantity": 1},
                    {"part_number": "CC-CLEAN", "description": "Condenser coil cleaner", "cost": "$25", "quantity": 1}
                ],
                "estimated_time": "30-60 minutes",
                "safety_precautions": [
                    "Ensure power is disconnected before maintenance",
                    "Wear protective gloves when handling refrigerant",
                    "Use proper ventilation when using cleaning chemicals"
                ]
            },
            
            "low_pressure": {
                "symptoms": "Pressure reading below 35 PSI, weak airflow",
                "possible_causes": [
                    "Duct leak or disconnection",
                    "Damper malfunction",
                    "Blower motor issue",
                    "Air filter blockage"
                ],
                "diagnosis_steps": [
                    "Inspect ductwork for leaks or gaps",
                    "Check damper positions and actuators",
                    "Test blower motor operation",
                    "Verify air filter is not blocked"
                ],
                "resolution": [
                    "Seal any duct leaks with approved duct sealant",
                    "Adjust or replace damper actuators",
                    "Service or replace blower motor if faulty",
                    "Replace air filter if needed"
                ],
                "required_parts": [
                    {"part_number": "DS-500", "description": "Duct sealant", "cost": "$30", "quantity": 1},
                    {"part_number": "DA-150", "description": "Damper actuator", "cost": "$85", "quantity": 1}
                ],
                "estimated_time": "1-2 hours",
                "safety_precautions": [
                    "Ensure system is powered off",
                    "Use ladder safety when accessing ductwork"
                ]
            },
            
            "high_current": {
                "symptoms": "Current draw above 15 Amps, circuit breaker trips",
                "possible_causes": [
                    "Motor bearing wear",
                    "Electrical short circuit",
                    "Capacitor failure",
                    "Compressor overload"
                ],
                "diagnosis_steps": [
                    "Check motor bearings for wear or noise",
                    "Inspect wiring for damage or shorts",
                    "Test start and run capacitors",
                    "Measure compressor current draw"
                ],
                "resolution": [
                    "Replace worn motor bearings",
                    "Repair or replace damaged wiring",
                    "Replace faulty capacitors",
                    "Service or replace compressor if overloaded"
                ],
                "required_parts": [
                    {"part_number": "MB-300", "description": "Motor bearing set", "cost": "$65", "quantity": 1},
                    {"part_number": "SC-45", "description": "Start capacitor 45µF", "cost": "$35", "quantity": 1},
                    {"part_number": "RC-35", "description": "Run capacitor 35µF", "cost": "$30", "quantity": 1}
                ],
                "estimated_time": "2-3 hours",
                "safety_precautions": [
                    "Disconnect all power before electrical work",
                    "Discharge capacitors before handling",
                    "Use insulated tools"
                ]
            }
        },
        
        "maintenance_schedule": """
        PREVENTIVE MAINTENANCE SCHEDULE:
        Monthly:
        - Inspect and clean/replace air filters
        - Check refrigerant levels
        - Verify temperature and pressure readings
        
        Quarterly:
        - Clean condenser coils
        - Inspect electrical connections
        - Test safety controls
        
        Annually:
        - Complete system inspection
        - Replace worn belts and bearings
        - Calibrate sensors
        - Professional refrigerant system check
        """
    },
    
    "MOTOR-001": {
        "equipment_name": "Industrial Conveyor Motor Model CM-500",
        "equipment_type": "Conveyor Motor",
        "manufacturer": "PowerDrive Systems",
        "model": "CM-500",
        "installation_date": "2023-03-20",
        
        "specifications": {
            "power_rating": "5 HP",
            "operating_speed": "1750 RPM",
            "voltage": "480V 3-phase",
            "normal_vibration": "0.5-2.0 Hz",
            "operating_temp_range": "40-60°C",
            "current_draw": "15-25 Amps"
        },
        
        "normal_parameters": """
        NORMAL OPERATING PARAMETERS:
        - Vibration: 0.5-2.0 Hz (optimal: 1.0-1.5 Hz)
        - Temperature: 40-60°C (optimal: 45-55°C)
        - Current Draw: 15-25 Amps (optimal: 18-22 Amps)
        - Speed: 1750 RPM ±50 RPM
        """,
        
        "troubleshooting": {
            "excessive_vibration": {
                "symptoms": "Vibration reading above 3.5 Hz, unusual noise, reduced performance",
                "possible_causes": [
                    "Worn or damaged roller bearings",
                    "Motor misalignment with conveyor shaft",
                    "Imbalanced load on conveyor",
                    "Loose mounting bolts",
                    "Bent or damaged motor shaft"
                ],
                "diagnosis_steps": [
                    "Inspect roller bearings for wear, noise, or heat",
                    "Check motor alignment using dial indicator",
                    "Verify load distribution on conveyor belt",
                    "Inspect and tighten all mounting bolts",
                    "Check motor shaft for straightness"
                ],
                "resolution": [
                    "Stop conveyor system immediately",
                    "Replace worn roller bearings (Part: RB-500)",
                    "Realign motor using alignment shims",
                    "Balance conveyor load distribution",
                    "Tighten all mounting bolts to spec (85 ft-lbs)",
                    "Replace motor shaft if bent",
                    "Restart and monitor vibration levels"
                ],
                "required_parts": [
                    {"part_number": "RB-500", "description": "Roller bearing set", "cost": "$120", "quantity": 2},
                    {"part_number": "AS-KIT", "description": "Alignment shim kit", "cost": "$45", "quantity": 1},
                    {"part_number": "MB-SET", "description": "Mounting bolt set", "cost": "$25", "quantity": 1}
                ],
                "estimated_time": "2-3 hours",
                "safety_precautions": [
                    "Lock out/tag out power before maintenance",
                    "Ensure conveyor is completely stopped",
                    "Use proper lifting equipment for heavy components",
                    "Wear safety glasses and gloves"
                ]
            },
            
            "overheating": {
                "symptoms": "Temperature above 75°C, burning smell, reduced efficiency",
                "possible_causes": [
                    "Motor overload condition",
                    "Poor ventilation or blocked cooling vents",
                    "Winding insulation failure",
                    "Excessive ambient temperature",
                    "Faulty cooling fan"
                ],
                "diagnosis_steps": [
                    "Check motor load - should not exceed rated capacity",
                    "Inspect cooling vents for blockage",
                    "Test winding resistance and insulation",
                    "Verify ambient temperature is within spec",
                    "Check cooling fan operation"
                ],
                "resolution": [
                    "Reduce motor load to rated capacity",
                    "Clean cooling vents and fan blades",
                    "Replace cooling fan if faulty (Part: CF-200)",
                    "Apply thermal paste to motor housing",
                    "Improve ventilation around motor",
                    "Monitor temperature for 1 hour after restart"
                ],
                "required_parts": [
                    {"part_number": "CF-200", "description": "Cooling fan assembly", "cost": "$95", "quantity": 1},
                    {"part_number": "TP-100", "description": "Thermal paste", "cost": "$15", "quantity": 1}
                ],
                "estimated_time": "1-2 hours",
                "safety_precautions": [
                    "Allow motor to cool before touching",
                    "Disconnect power before maintenance",
                    "Use heat-resistant gloves"
                ]
            },
            
            "high_current": {
                "symptoms": "Current draw above 30 Amps, circuit breaker trips, reduced speed",
                "possible_causes": [
                    "Mechanical binding or obstruction",
                    "Phase imbalance in power supply",
                    "Winding insulation breakdown",
                    "Overloaded conveyor",
                    "Faulty motor contactor"
                ],
                "diagnosis_steps": [
                    "Check for mechanical obstructions",
                    "Measure voltage on all three phases",
                    "Test winding insulation resistance",
                    "Verify conveyor load is within limits",
                    "Inspect motor contactor contacts"
                ],
                "resolution": [
                    "Remove any mechanical obstructions",
                    "Balance three-phase power supply",
                    "Replace motor if winding failure detected",
                    "Reduce conveyor load",
                    "Replace motor contactor if faulty (Part: MC-75)"
                ],
                "required_parts": [
                    {"part_number": "MC-75", "description": "Motor contactor 75A", "cost": "$150", "quantity": 1},
                    {"part_number": "IT-TAPE", "description": "Insulation tape", "cost": "$20", "quantity": 1}
                ],
                "estimated_time": "2-4 hours",
                "safety_precautions": [
                    "Lock out/tag out all power sources",
                    "Test for voltage before touching",
                    "Use insulated tools",
                    "Have qualified electrician present"
                ]
            }
        },
        
        "maintenance_schedule": """
        PREVENTIVE MAINTENANCE SCHEDULE:
        Weekly:
        - Check vibration levels
        - Inspect for unusual noise
        - Verify temperature readings
        
        Monthly:
        - Lubricate bearings
        - Check motor alignment
        - Inspect electrical connections
        - Clean cooling vents
        
        Quarterly:
        - Replace bearing grease
        - Test insulation resistance
        - Inspect conveyor belt condition
        
        Annually:
        - Complete motor inspection
        - Replace bearings
        - Professional alignment check
        - Thermal imaging inspection
        """
    }
}


def get_manual(equipment_id):
    """
    Get equipment manual by ID
    
    Args:
        equipment_id: Equipment identifier (e.g., 'HVAC-001')
    
    Returns:
        dict: Manual content
    """
    if equipment_id not in MANUAL_CONTENT:
        raise ValueError(f"No manual found for equipment: {equipment_id}")
    
    return MANUAL_CONTENT[equipment_id]


def get_troubleshooting_section(equipment_id, issue_type):
    """
    Get specific troubleshooting section
    
    Args:
        equipment_id: Equipment identifier
        issue_type: Type of issue (e.g., 'overheating', 'excessive_vibration')
    
    Returns:
        dict: Troubleshooting information
    """
    manual = get_manual(equipment_id)
    
    if issue_type not in manual["troubleshooting"]:
        # Return generic troubleshooting if specific issue not found
        return {
            "symptoms": f"Issue detected: {issue_type}",
            "possible_causes": ["Unknown cause - requires inspection"],
            "resolution": ["Contact maintenance technician for inspection"],
            "required_parts": [],
            "estimated_time": "Unknown",
            "safety_precautions": ["Follow standard safety procedures"]
        }
    
    return manual["troubleshooting"][issue_type]


def search_manual_content(equipment_id, query):
    """
    Simple keyword search in manual content (mock RAG for POC)
    
    Args:
        equipment_id: Equipment identifier
        query: Search query string
    
    Returns:
        list: Relevant sections
    """
    manual = get_manual(equipment_id)
    results = []
    
    query_lower = query.lower()
    
    # Search in troubleshooting sections
    for issue_type, content in manual["troubleshooting"].items():
        # Check if query matches issue type or symptoms
        if query_lower in issue_type.lower() or query_lower in content["symptoms"].lower():
            results.append({
                "section": "troubleshooting",
                "issue_type": issue_type,
                "content": content,
                "relevance": "high"
            })
    
    return results


# Quick test
if __name__ == "__main__":
    print("=== Testing Equipment Manuals ===\n")
    
    # Test HVAC manual
    print("HVAC-001 Manual:")
    hvac_manual = get_manual("HVAC-001")
    print(f"Equipment: {hvac_manual['equipment_name']}")
    print(f"Model: {hvac_manual['model']}")
    print(f"Manufacturer: {hvac_manual['manufacturer']}")
    
    print("\nTroubleshooting - Overheating:")
    overheating = get_troubleshooting_section("HVAC-001", "overheating")
    print(f"Symptoms: {overheating['symptoms']}")
    print(f"Required Parts: {len(overheating['required_parts'])} items")
    for part in overheating['required_parts']:
        print(f"  - {part['part_number']}: {part['description']} (${part['cost']})")
    
    print("\n" + "="*50 + "\n")
    
    # Test Motor manual
    print("MOTOR-001 Manual:")
    motor_manual = get_manual("MOTOR-001")
    print(f"Equipment: {motor_manual['equipment_name']}")
    print(f"Model: {motor_manual['model']}")
    
    print("\nTroubleshooting - Excessive Vibration:")
    vibration = get_troubleshooting_section("MOTOR-001", "excessive_vibration")
    print(f"Symptoms: {vibration['symptoms']}")
    print(f"Estimated Time: {vibration['estimated_time']}")
    print(f"Required Parts: {len(vibration['required_parts'])} items")
    for part in vibration['required_parts']:
        print(f"  - {part['part_number']}: {part['description']} (${part['cost']})")
    
    print("\n" + "="*50 + "\n")
    
    # Test search
    print("Search Test - 'overheating':")
    results = search_manual_content("HVAC-001", "overheating")
    print(f"Found {len(results)} results")
    for result in results:
        print(f"  - {result['section']}: {result['issue_type']} (relevance: {result['relevance']})")

# Made with Bob
