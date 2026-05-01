"""
Mock API Server for SyncOpsAI Demo
Simulates watsonx Orchestrate agent and tool endpoints
"""

from flask import Flask, request, jsonify
from datetime import datetime
import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagnosis import diagnose
from data import check_anomaly

app = Flask(__name__)

# Store work orders in memory (for demo)
work_orders = {}
work_order_counter = 1000


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SyncOpsAI Mock API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/tools/detect_anomaly', methods=['POST'])
def detect_anomaly():
    """
    Detect anomalies in sensor data
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        }
    }
    """
    try:
        data = request.json
        equipment_id = data.get('equipment_id')
        sensor_data = data.get('sensor_data')
        
        if not equipment_id or not sensor_data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Determine scenario from equipment_id
        scenario_map = {
            "HVAC-001": "hvac_overheating",
            "HVAC-002": "hvac_overheating",
            "MOTOR-001": "motor_vibration",
            "MOTOR-002": "motor_vibration"
        }
        scenario_name = scenario_map.get(equipment_id, "hvac_overheating")
        
        # Check for anomaly
        is_anomaly, anomaly_type, severity = check_anomaly(scenario_name, sensor_data)
        
        result = {
            'anomaly_detected': is_anomaly,
            'anomaly_type': anomaly_type if is_anomaly else None,
            'severity': severity,
            'equipment_id': equipment_id,
            'sensor_data': sensor_data
        }
        
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/generate_diagnosis', methods=['POST'])
def generate_diagnosis():
    """
    Generate diagnostic report
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "anomaly_type": "overheating",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        },
        "use_ai": false,
        "use_pinecone": false
    }
    """
    try:
        data = request.json
        equipment_id = data.get('equipment_id')
        anomaly_type = data.get('anomaly_type')
        sensor_data = data.get('sensor_data')
        use_ai = data.get('use_ai', False)
        use_pinecone = data.get('use_pinecone', False)
        
        if not equipment_id or not anomaly_type or not sensor_data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Use our existing diagnosis function
        result = diagnose(
            equipment_id=equipment_id,
            anomaly_type=anomaly_type,
            sensor_data=sensor_data,
            use_ai=use_ai,
            use_pinecone=use_pinecone
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/create_work_order', methods=['POST'])
def create_work_order():
    """
    Create maintenance work order
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "root_cause": "Clogged air filter",
        "severity": "medium",
        "resolution_steps": ["Step 1", "Step 2"],
        "required_parts": [{"part_number": "FILTER-001", "quantity": 1}],
        "estimated_cost": "$45.00"
    }
    """
    try:
        global work_order_counter
        data = request.json
        
        equipment_id = data.get('equipment_id')
        root_cause = data.get('root_cause')
        severity = data.get('severity', 'medium')
        
        if not equipment_id or not root_cause:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate work order ID
        work_order_id = f'WO-{work_order_counter}'
        work_order_counter += 1
        
        # Priority mapping
        priority_map = {
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'critical': 'Critical'
        }
        priority = priority_map.get(severity.lower(), 'Medium')
        
        # Completion hours
        completion_hours = {
            'low': 48,
            'medium': 24,
            'high': 8,
            'critical': 4
        }
        hours = completion_hours.get(severity.lower(), 24)
        
        # Assign team
        if 'HVAC' in equipment_id:
            assigned_to = 'HVAC Specialist Team'
        elif 'MOTOR' in equipment_id:
            assigned_to = 'Motor Maintenance Team'
        else:
            assigned_to = 'General Maintenance Team'
        
        work_order = {
            'work_order_id': work_order_id,
            'equipment_id': equipment_id,
            'status': 'Open',
            'priority': priority,
            'root_cause': root_cause,
            'resolution_steps': data.get('resolution_steps', []),
            'required_parts': data.get('required_parts', []),
            'estimated_cost': data.get('estimated_cost', '$0.00'),
            'created_at': datetime.now().isoformat(),
            'estimated_completion_hours': hours,
            'assigned_to': assigned_to,
            'parts_ordered': len(data.get('required_parts', [])) > 0
        }
        
        # Store work order
        work_orders[work_order_id] = work_order
        
        return jsonify({
            'success': True,
            'result': work_order,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/check_inventory', methods=['POST'])
def check_inventory():
    """
    Check parts inventory
    
    Request body:
    {
        "required_parts": [
            {"part_number": "FILTER-001", "name": "Air Filter", "quantity": 1, "cost": "$45"}
        ]
    }
    """
    try:
        data = request.json
        required_parts = data.get('required_parts', [])
        
        # Mock inventory
        inventory = {
            'FILTER-001': {'stock': 25, 'location': 'Warehouse A', 'unit_cost': 45.00},
            'BEARING-001': {'stock': 8, 'location': 'Warehouse B', 'unit_cost': 120.00},
            'BELT-001': {'stock': 0, 'location': 'Warehouse A', 'unit_cost': 35.00},
            'SENSOR-001': {'stock': 15, 'location': 'Warehouse C', 'unit_cost': 85.00}
        }
        
        parts_status = []
        all_available = True
        total_value = 0.0
        max_delivery_days = 0
        
        for part in required_parts:
            part_number = part.get('part_number')
            quantity_needed = part.get('quantity', 1)
            
            if part_number in inventory:
                inv_item = inventory[part_number]
                stock = inv_item['stock']
                available = stock >= quantity_needed
                
                if not available:
                    all_available = False
                    delivery_days = 3
                    max_delivery_days = max(max_delivery_days, delivery_days)
                else:
                    delivery_days = 0
                
                cost_str = part.get('cost', f"${inv_item['unit_cost']}")
                unit_cost = float(cost_str.replace('$', ''))
                total_value += unit_cost * quantity_needed
                
                parts_status.append({
                    'part_number': part_number,
                    'name': part.get('name', 'Unknown Part'),
                    'quantity_needed': quantity_needed,
                    'quantity_available': stock,
                    'available': available,
                    'location': inv_item['location'],
                    'unit_cost': f"${inv_item['unit_cost']:.2f}",
                    'total_cost': f"${unit_cost * quantity_needed:.2f}",
                    'delivery_days': delivery_days
                })
            else:
                all_available = False
                max_delivery_days = max(max_delivery_days, 7)
                
                parts_status.append({
                    'part_number': part_number,
                    'name': part.get('name', 'Unknown Part'),
                    'quantity_needed': quantity_needed,
                    'quantity_available': 0,
                    'available': False,
                    'location': 'Not in inventory',
                    'unit_cost': part.get('cost', '$0.00'),
                    'total_cost': '$0.00',
                    'delivery_days': 7
                })
        
        if all_available:
            estimated_delivery = 'All parts available - immediate pickup'
        elif max_delivery_days <= 3:
            estimated_delivery = f'{max_delivery_days} business days'
        else:
            estimated_delivery = f'{max_delivery_days} business days (special order)'
        
        result = {
            'parts_status': parts_status,
            'all_available': all_available,
            'total_value': f'${total_value:.2f}',
            'estimated_delivery': estimated_delivery,
            'parts_to_order': [p for p in parts_status if not p['available']]
        }
        
        return jsonify({
            'success': True,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agents/telemetry', methods=['POST'])
def telemetry_agent():
    """
    Telemetry Agent endpoint - monitors sensor data
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        }
    }
    """
    try:
        data = request.json
        equipment_id = data.get('equipment_id')
        sensor_data = data.get('sensor_data')
        
        # Determine scenario and check for anomaly
        scenario_map = {
            "HVAC-001": "hvac_overheating",
            "HVAC-002": "hvac_overheating",
            "MOTOR-001": "motor_vibration",
            "MOTOR-002": "motor_vibration"
        }
        scenario_name = scenario_map.get(equipment_id, "hvac_overheating")
        is_anomaly, anomaly_type, severity = check_anomaly(scenario_name, sensor_data)
        
        anomaly_result = {
            'anomaly_detected': is_anomaly,
            'anomaly_type': anomaly_type if is_anomaly else None,
            'severity': severity,
            'equipment_id': equipment_id,
            'sensor_data': sensor_data
        }
        
        response = {
            'agent': 'telemetry_listener_agent',
            'action': 'anomaly_detection',
            'result': anomaly_result,
            'next_agent': 'diagnostic_expert_agent' if anomaly_result['anomaly_detected'] else None,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agents/diagnostic', methods=['POST'])
def diagnostic_agent():
    """
    Diagnostic Agent endpoint - generates diagnosis
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "anomaly_type": "overheating",
        "sensor_data": {...},
        "use_ai": false
    }
    """
    try:
        data = request.json
        
        # Generate diagnosis
        diagnosis_result = diagnose(
            equipment_id=data.get('equipment_id'),
            anomaly_type=data.get('anomaly_type'),
            sensor_data=data.get('sensor_data'),
            use_ai=data.get('use_ai', False),
            use_pinecone=data.get('use_pinecone', False)
        )
        
        response = {
            'agent': 'diagnostic_expert_agent',
            'action': 'diagnosis_generation',
            'result': diagnosis_result,
            'next_agent': 'orchestrator_agent',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agents/orchestrator', methods=['POST'])
def orchestrator_agent():
    """
    Orchestrator Agent endpoint - creates work orders
    
    Request body:
    {
        "diagnosis": {...}
    }
    """
    try:
        data = request.json
        diagnosis = data.get('diagnosis')
        
        if not diagnosis:
            return jsonify({'error': 'Missing diagnosis'}), 400
        
        # Check inventory
        inventory_result = check_inventory().get_json()
        
        # Create work order
        work_order_result = create_work_order().get_json()
        
        response = {
            'agent': 'orchestrator_agent',
            'action': 'work_order_creation',
            'inventory_check': inventory_result.get('result'),
            'work_order': work_order_result.get('result'),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/workflow/run', methods=['POST'])
def run_workflow():
    """
    Run complete multi-agent workflow
    
    Request body:
    {
        "equipment_id": "HVAC-001",
        "sensor_data": {...},
        "use_ai": false,
        "use_pinecone": false
    }
    """
    try:
        data = request.json
        equipment_id = data.get('equipment_id')
        sensor_data = data.get('sensor_data')
        use_ai = data.get('use_ai', False)
        use_pinecone = data.get('use_pinecone', False)
        
        workflow_steps = []
        
        # Step 1: Telemetry Agent - Detect anomaly
        scenario_map = {
            "HVAC-001": "hvac_overheating",
            "HVAC-002": "hvac_overheating",
            "MOTOR-001": "motor_vibration",
            "MOTOR-002": "motor_vibration"
        }
        scenario_name = scenario_map.get(equipment_id, "hvac_overheating")
        
        # If no sensor data provided, get the latest reading from the scenario
        if sensor_data is None:
            from data import get_latest_reading
            sensor_data = get_latest_reading(scenario_name)
        
        is_anomaly, anomaly_type, severity = check_anomaly(scenario_name, sensor_data)
        
        anomaly_result = {
            'anomaly_detected': is_anomaly,
            'anomaly_type': anomaly_type if is_anomaly else None,
            'severity': severity,
            'equipment_id': equipment_id,
            'sensor_data': sensor_data
        }
        workflow_steps.append({
            'step': 1,
            'agent': 'telemetry_listener_agent',
            'action': 'anomaly_detection',
            'result': anomaly_result
        })
        
        if not anomaly_result['anomaly_detected']:
            return jsonify({
                'success': True,
                'workflow_complete': True,
                'steps': workflow_steps,
                'message': 'No anomaly detected',
                'timestamp': datetime.now().isoformat()
            })
        
        # Step 2: Diagnostic Agent
        try:
            diagnosis_result = diagnose(
                equipment_id=equipment_id,
                anomaly_type=anomaly_result['anomaly_type'],
                sensor_data=sensor_data,
                use_ai=use_ai,
                use_pinecone=use_pinecone
            )
            
            # Ensure diagnosis_result is not None
            if diagnosis_result is None:
                raise ValueError("Diagnosis returned None")
                
        except Exception as e:
            # Fallback to template-based diagnosis
            print(f"Diagnosis error: {e}, using fallback")
            diagnosis_result = {
                'root_cause': f'Anomaly detected: {anomaly_result["anomaly_type"]}',
                'severity': 'high',
                'resolution_steps': [
                    'Inspect equipment immediately',
                    'Check sensor readings',
                    'Contact maintenance team'
                ],
                'required_parts': [],
                'estimated_cost': '$150',
                'confidence': 0.75
            }
        
        workflow_steps.append({
            'step': 2,
            'agent': 'diagnostic_expert_agent',
            'action': 'diagnosis_generation',
            'result': diagnosis_result
        })
        
        # Step 3: Orchestrator Agent - Check Inventory
        required_parts = diagnosis_result.get('required_parts', [])
        
        # Mock inventory check logic (same as check_inventory endpoint)
        inventory = {
            'FILTER-001': {'stock': 25, 'location': 'Warehouse A', 'unit_cost': 45.00},
            'BEARING-001': {'stock': 8, 'location': 'Warehouse B', 'unit_cost': 120.00},
        }
        
        parts_status = []
        all_available = True
        for part in required_parts:
            part_number = part.get('part_number')
            if part_number in inventory:
                inv_item = inventory[part_number]
                parts_status.append({
                    'part_number': part_number,
                    'available': True,
                    'stock': inv_item['stock']
                })
            else:
                all_available = False
                parts_status.append({
                    'part_number': part_number,
                    'available': False,
                    'stock': 0
                })
        
        inventory_result = {
            'parts_status': parts_status,
            'all_available': all_available
        }
        
        workflow_steps.append({
            'step': 3,
            'agent': 'orchestrator_agent',
            'action': 'inventory_check',
            'result': inventory_result
        })
        
        # Step 4: Orchestrator Agent - Create Work Order
        global work_order_counter
        work_order_id = f'WO-{work_order_counter}'
        work_order_counter += 1
        
        # Assign team based on equipment type
        if 'HVAC' in equipment_id:
            assigned_to = 'HVAC Specialist Team'
        elif 'MOTOR' in equipment_id:
            assigned_to = 'Motor Maintenance Team'
        else:
            assigned_to = 'General Maintenance Team'
        
        # Determine completion hours based on severity
        completion_hours = {
            'low': 48,
            'medium': 24,
            'high': 8,
            'critical': 4
        }
        hours = completion_hours.get(diagnosis_result['severity'].lower(), 24)
        
        work_order_result = {
            'work_order_id': work_order_id,
            'equipment_id': equipment_id,
            'status': 'Open',
            'priority': 'High' if diagnosis_result['severity'] == 'critical' else 'Medium',
            'root_cause': diagnosis_result['root_cause'],
            'resolution_steps': diagnosis_result['resolution_steps'],
            'required_parts': diagnosis_result.get('required_parts', []),
            'estimated_cost': diagnosis_result['estimated_cost'],
            'created_at': datetime.now().isoformat(),
            'estimated_completion_hours': hours,
            'assigned_to': assigned_to,
            'parts_ordered': len(diagnosis_result.get('required_parts', [])) > 0
        }
        
        # Store work order in global dictionary
        work_orders[work_order_id] = work_order_result
        
        workflow_steps.append({
            'step': 4,
            'agent': 'orchestrator_agent',
            'action': 'work_order_creation',
            'result': work_order_result
        })
        
        return jsonify({
            'success': True,
            'workflow_complete': True,
            'steps': workflow_steps,
            'summary': {
                'anomaly_detected': True,
                'anomaly_type': anomaly_result['anomaly_type'],
                'severity': diagnosis_result['severity'],
                'work_order_id': work_order_id,
                'estimated_cost': diagnosis_result['estimated_cost']
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/work_orders', methods=['GET'])
def get_work_orders():
    """Get all work orders"""
    return jsonify({
        'success': True,
        'work_orders': list(work_orders.values()),
        'count': len(work_orders),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/work_orders/<work_order_id>', methods=['GET'])
def get_work_order(work_order_id):
    """Get specific work order"""
    if work_order_id in work_orders:
        return jsonify({
            'success': True,
            'work_order': work_orders[work_order_id],
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': 'Work order not found'}), 404


if __name__ == '__main__':
    print("Starting SyncOpsAI Mock API Server...")
    print("Server running on http://localhost:8787")
    print("\nAvailable endpoints:")
    print("  GET  /health")
    print("  POST /api/tools/detect_anomaly")
    print("  POST /api/tools/generate_diagnosis")
    print("  POST /api/tools/create_work_order")
    print("  POST /api/tools/check_inventory")
    print("  POST /api/agents/telemetry")
    print("  POST /api/agents/diagnostic")
    print("  POST /api/agents/orchestrator")
    print("  POST /api/workflow/run")
    print("  GET  /api/work_orders")
    print("  GET  /api/work_orders/<id>")
    print("\nPress Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=8787)

# Made with Bob
