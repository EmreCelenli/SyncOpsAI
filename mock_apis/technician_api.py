"""
Mock Technician Management System API
For hackathon demo - simulates real technician dispatch system
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock technician data
technicians = {
    "TECH-001": {
        "name": "John Smith",
        "specialization": "HVAC",
        "status": "available",
        "location": "Zone A",
        "skill_level": "senior"
    },
    "TECH-002": {
        "name": "Sarah Johnson",
        "specialization": "Motors",
        "status": "available",
        "location": "Zone B",
        "skill_level": "senior"
    },
    "TECH-003": {
        "name": "Mike Chen",
        "specialization": "HVAC",
        "status": "on_job",
        "location": "Zone C",
        "skill_level": "intermediate"
    },
    "TECH-004": {
        "name": "Emily Davis",
        "specialization": "Motors",
        "status": "available",
        "location": "Zone A",
        "skill_level": "expert"
    }
}

@app.route('/api/v1/technicians/find', methods=['POST'])
def find_technician():
    """Find available technician based on requirements"""
    data = request.json
    equipment_type = data.get('equipment_type', '').lower()
    priority = data.get('priority', 'medium')
    location = data.get('location', 'Zone A')
    
    # Map equipment types to specializations
    specialization_map = {
        'hvac': 'HVAC',
        'motor': 'Motors',
        'conveyor': 'Motors'
    }
    
    required_specialization = specialization_map.get(equipment_type, 'HVAC')
    
    # Find available technicians with matching specialization
    available = []
    for tech_id, tech_data in technicians.items():
        if (tech_data['status'] == 'available' and 
            tech_data['specialization'] == required_specialization):
            available.append({
                'technician_id': tech_id,
                'name': tech_data['name'],
                'specialization': tech_data['specialization'],
                'skill_level': tech_data['skill_level'],
                'location': tech_data['location'],
                'estimated_arrival': (datetime.now() + timedelta(minutes=random.randint(15, 45))).isoformat()
            })
    
    if not available:
        return jsonify({
            'found': False,
            'message': f'No available {required_specialization} technicians',
            'next_available': (datetime.now() + timedelta(hours=2)).isoformat()
        }), 200
    
    # Sort by skill level (expert > senior > intermediate)
    skill_priority = {'expert': 3, 'senior': 2, 'intermediate': 1}
    available.sort(key=lambda x: skill_priority.get(x['skill_level'], 0), reverse=True)
    
    return jsonify({
        'found': True,
        'technician': available[0],
        'alternatives': available[1:] if len(available) > 1 else []
    }), 200

@app.route('/api/v1/technicians/assign', methods=['POST'])
def assign_technician():
    """Assign technician to a work order"""
    data = request.json
    technician_id = data.get('technician_id')
    work_order_id = data.get('work_order_id')
    
    if technician_id not in technicians:
        return jsonify({'error': 'Technician not found'}), 404
    
    tech_data = technicians[technician_id]
    
    # Update technician status
    technicians[technician_id]['status'] = 'assigned'
    
    assignment_id = f"ASSIGN-{random.randint(1000, 9999)}"
    
    response = {
        'assignment_id': assignment_id,
        'technician_id': technician_id,
        'technician_name': tech_data['name'],
        'work_order_id': work_order_id,
        'status': 'assigned',
        'estimated_arrival': (datetime.now() + timedelta(minutes=30)).isoformat(),
        'assigned_at': datetime.now().isoformat()
    }
    
    return jsonify(response), 200

@app.route('/api/v1/technicians/<technician_id>', methods=['GET'])
def get_technician(technician_id):
    """Get technician details"""
    if technician_id not in technicians:
        return jsonify({'error': 'Technician not found'}), 404
    
    tech_data = technicians[technician_id]
    response = {
        'technician_id': technician_id,
        **tech_data,
        'certifications': ['HVAC-Pro', 'Safety-Level-2'],
        'years_experience': random.randint(3, 15)
    }
    
    return jsonify(response), 200

@app.route('/api/v1/technicians', methods=['GET'])
def list_technicians():
    """List all technicians"""
    tech_list = []
    for tech_id, tech_data in technicians.items():
        tech_list.append({
            'technician_id': tech_id,
            **tech_data
        })
    
    return jsonify({'technicians': tech_list, 'total': len(tech_list)}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'service': 'technician_api'}), 200

if __name__ == '__main__':
    print("👷 Mock Technician API starting on http://localhost:5003")
    print("   POST   /api/v1/technicians/find - Find available technician")
    print("   POST   /api/v1/technicians/assign - Assign to work order")
    print("   GET    /api/v1/technicians/<id> - Get technician details")
    print("   GET    /api/v1/technicians - List all technicians")
    app.run(host='0.0.0.0', port=5003, debug=True)

# Made with Bob
