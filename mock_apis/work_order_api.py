"""
Mock Work Order Management System API
For hackathon demo - simulates real work order system
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# In-memory storage for demo
work_orders = {}

@app.route('/api/v1/work-orders', methods=['POST'])
def create_work_order():
    """Create a new work order"""
    data = request.json
    
    work_order_id = f"WO-{uuid.uuid4().hex[:6].upper()}"
    
    work_order = {
        'work_order_id': work_order_id,
        'equipment_id': data.get('equipment_id'),
        'issue_description': data.get('issue_description'),
        'required_parts': data.get('required_parts', []),
        'priority': data.get('priority', 'high'),
        'status': 'open',
        'assigned_to': 'auto-assign',
        'estimated_completion': '2-4 hours',
        'created_at': datetime.now().isoformat(),
        'created_by': data.get('created_by', 'ai_agent')
    }
    
    work_orders[work_order_id] = work_order
    
    return jsonify(work_order), 201

@app.route('/api/v1/work-orders/<work_order_id>', methods=['GET'])
def get_work_order(work_order_id):
    """Get work order details"""
    if work_order_id not in work_orders:
        return jsonify({'error': 'Work order not found'}), 404
    
    return jsonify(work_orders[work_order_id]), 200

@app.route('/api/v1/work-orders/<work_order_id>', methods=['PATCH'])
def update_work_order(work_order_id):
    """Update work order"""
    if work_order_id not in work_orders:
        return jsonify({'error': 'Work order not found'}), 404
    
    data = request.json
    work_order = work_orders[work_order_id]
    
    if 'status' in data:
        work_order['status'] = data['status']
    if 'assigned_to' in data:
        work_order['assigned_to'] = data['assigned_to']
    if 'notes' in data:
        work_order['notes'] = data['notes']
    
    work_order['updated_at'] = datetime.now().isoformat()
    
    return jsonify(work_order), 200

@app.route('/api/v1/work-orders', methods=['GET'])
def list_work_orders():
    """List all work orders"""
    return jsonify({'work_orders': list(work_orders.values())}), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'service': 'work_order_api'}), 200

if __name__ == '__main__':
    print("🔧 Mock Work Order API starting on http://localhost:5001")
    print("   POST   /api/v1/work-orders - Create work order")
    print("   GET    /api/v1/work-orders/<id> - Get work order")
    print("   PATCH  /api/v1/work-orders/<id> - Update work order")
    print("   GET    /api/v1/work-orders - List all work orders")
    app.run(host='0.0.0.0', port=5001, debug=True)

# Made with Bob
