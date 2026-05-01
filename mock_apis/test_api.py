"""
Test script for SyncOpsAI Mock API
"""

import requests
import json

BASE_URL = "http://localhost:8787"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)


def test_detect_anomaly():
    """Test anomaly detection"""
    data = {
        "equipment_id": "HVAC-001",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        }
    }
    response = requests.post(f"{BASE_URL}/api/tools/detect_anomaly", json=data)
    print_response("Detect Anomaly", response)
    return response.json()


def test_generate_diagnosis():
    """Test diagnosis generation"""
    data = {
        "equipment_id": "HVAC-001",
        "anomaly_type": "overheating",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        },
        "use_ai": False,
        "use_pinecone": False
    }
    response = requests.post(f"{BASE_URL}/api/tools/generate_diagnosis", json=data)
    print_response("Generate Diagnosis", response)
    return response.json()


def test_check_inventory():
    """Test inventory check"""
    data = {
        "required_parts": [
            {
                "part_number": "FILTER-001",
                "name": "Air Filter",
                "quantity": 1,
                "cost": "$45"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/tools/check_inventory", json=data)
    print_response("Check Inventory", response)
    return response.json()


def test_create_work_order():
    """Test work order creation"""
    data = {
        "equipment_id": "HVAC-001",
        "root_cause": "Clogged air filter",
        "severity": "medium",
        "resolution_steps": [
            "Turn off HVAC system",
            "Remove and inspect air filter",
            "Replace filter if clogged"
        ],
        "required_parts": [
            {
                "part_number": "FILTER-001",
                "name": "Air Filter",
                "quantity": 1,
                "cost": "$45"
            }
        ],
        "estimated_cost": "$45.00"
    }
    response = requests.post(f"{BASE_URL}/api/tools/create_work_order", json=data)
    print_response("Create Work Order", response)
    return response.json()


def test_complete_workflow():
    """Test complete multi-agent workflow"""
    data = {
        "equipment_id": "HVAC-001",
        "sensor_data": {
            "temperature": 88,
            "pressure": 42
        },
        "use_ai": False,
        "use_pinecone": False
    }
    response = requests.post(f"{BASE_URL}/api/workflow/run", json=data)
    print_response("Complete Workflow", response)
    return response.json()


def test_get_work_orders():
    """Test getting all work orders"""
    response = requests.get(f"{BASE_URL}/api/work_orders")
    print_response("Get All Work Orders", response)


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("SyncOpsAI Mock API Test Suite")
    print("="*60)
    
    try:
        # Test 1: Health Check
        test_health()
        
        # Test 2: Individual Tools
        test_detect_anomaly()
        test_generate_diagnosis()
        test_check_inventory()
        test_create_work_order()
        
        # Test 3: Complete Workflow
        test_complete_workflow()
        
        # Test 4: Work Order Management
        test_get_work_orders()
        
        print("\n" + "="*60)
        print("All tests completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()

# Made with Bob
