"""
Mock Inventory Management System API
For hackathon demo - simulates real inventory system
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock inventory data
inventory = {
    "Air Filter AF-2024": {"quantity": 15, "location": "Warehouse A", "cost": 45.00},
    "Bearing RB-500": {"quantity": 8, "location": "Warehouse B", "cost": 120.00},
    "Compressor Seal Kit CS-2024": {"quantity": 5, "location": "Warehouse A", "cost": 85.00},
    "Refrigerant R-410A": {"quantity": 20, "location": "Warehouse C", "cost": 120.00},
    "Motor Belt MB-100": {"quantity": 12, "location": "Warehouse B", "cost": 35.00},
    "Thermostat TH-500": {"quantity": 10, "location": "Warehouse A", "cost": 75.00}
}

@app.route('/api/v1/inventory/check', methods=['POST'])
def check_availability():
    """Check parts availability"""
    data = request.json
    parts = data.get('parts', [])
    
    parts_status = []
    backorder_items = []
    all_available = True
    
    for part in parts:
        # Extract part number from string like "Air Filter AF-2024 ($45)"
        part_number = part.split('(')[0].strip() if '(' in part else part.strip()
        
        if part_number in inventory:
            inv_data = inventory[part_number]
            available = inv_data['quantity'] > 0
            parts_status.append({
                'part': part_number,
                'available': available,
                'quantity': inv_data['quantity'],
                'location': inv_data['location']
            })
            if not available:
                all_available = False
                backorder_items.append(part_number)
        else:
            # Unknown part - assume available for demo
            parts_status.append({
                'part': part_number,
                'available': True,
                'quantity': 5,
                'location': 'Warehouse A'
            })
    
    response = {
        'all_available': all_available,
        'parts_status': parts_status,
        'backorder_items': backorder_items,
        'estimated_delivery': None if all_available else (datetime.now() + timedelta(days=3)).isoformat()
    }
    
    return jsonify(response), 200

@app.route('/api/v1/inventory/reserve', methods=['POST'])
def reserve_parts():
    """Reserve parts for a work order"""
    data = request.json
    work_order_id = data.get('work_order_id')
    parts = data.get('parts', [])
    
    reservation_id = f"RES-{random.randint(1000, 9999)}"
    
    response = {
        'reservation_id': reservation_id,
        'work_order_id': work_order_id,
        'status': 'reserved',
        'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
    }
    
    return jsonify(response), 200

@app.route('/api/v1/inventory/parts/<part_number>', methods=['GET'])
def get_part_details(part_number):
    """Get detailed information about a part"""
    if part_number not in inventory:
        return jsonify({'error': 'Part not found'}), 404
    
    inv_data = inventory[part_number]
    response = {
        'part_number': part_number,
        'description': f"Description for {part_number}",
        'quantity_available': inv_data['quantity'],
        'unit_cost': inv_data['cost'],
        'location': inv_data['location'],
        'supplier': 'Demo Supplier Inc.'
    }
    
    return jsonify(response), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'service': 'inventory_api'}), 200

if __name__ == '__main__':
    print("📦 Mock Inventory API starting on http://localhost:5002")
    print("   POST   /api/v1/inventory/check - Check availability")
    print("   POST   /api/v1/inventory/reserve - Reserve parts")
    print("   GET    /api/v1/inventory/parts/<part> - Get part details")
    app.run(host='0.0.0.0', port=5002, debug=True)

# Made with Bob
