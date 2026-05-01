"""
Inventory Check Tool for watsonx Orchestrate
Checks parts inventory and availability for maintenance work orders
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Dict, Any, List


@tool(
    name="check_inventory",
    display_name="Check Parts Inventory",
    description="Checks inventory availability for required maintenance parts. Returns stock levels, availability status, and estimated delivery times."
)
def check_inventory(required_parts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check inventory availability for required parts.
    
    Args:
        required_parts (list): List of parts with part_number, name, and quantity needed
    
    Returns:
        dict: Inventory status containing:
            - parts_status (list): Status for each requested part
            - all_available (bool): Whether all parts are in stock
            - total_value (str): Total value of parts
            - estimated_delivery (str): Delivery estimate for out-of-stock items
    """
    
    # Mock inventory database (in real system, this would query actual inventory)
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
                delivery_days = 3  # Standard delivery time for out-of-stock items
                max_delivery_days = max(max_delivery_days, delivery_days)
            else:
                delivery_days = 0
            
            # Calculate cost
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
            # Part not in inventory
            all_available = False
            max_delivery_days = max(max_delivery_days, 7)  # Longer delivery for unknown parts
            
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
    
    # Determine delivery estimate
    if all_available:
        estimated_delivery = 'All parts available - immediate pickup'
    elif max_delivery_days <= 3:
        estimated_delivery = f'{max_delivery_days} business days'
    else:
        estimated_delivery = f'{max_delivery_days} business days (special order)'
    
    return {
        'parts_status': parts_status,
        'all_available': all_available,
        'total_value': f'${total_value:.2f}',
        'estimated_delivery': estimated_delivery,
        'parts_to_order': [p for p in parts_status if not p['available']]
    }

# Made with Bob
