# SyncOpsAI Mock API Server

Mock REST API server that simulates watsonx Orchestrate agent and tool endpoints for demo purposes.

## 🎯 Purpose

This mock API allows you to demonstrate the SyncOpsAI multi-agent system without requiring actual watsonx Orchestrate deployment. It provides the same functionality through REST endpoints that can be called from any client (dashboard, CLI, etc.).

## 📦 Installation

```bash
cd mock_apis
pip install -r requirements.txt
```

## 🚀 Running the Server

```bash
python app.py
```

Server will start on `http://localhost:8787`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Tool Endpoints

#### 1. Detect Anomaly
```bash
POST /api/tools/detect_anomaly
Content-Type: application/json

{
  "equipment_id": "HVAC-001",
  "sensor_data": {
    "temperature": 88,
    "pressure": 42
  }
}
```

**Base URL:** `http://localhost:8787`

#### 2. Generate Diagnosis
```bash
POST /api/tools/generate_diagnosis
Content-Type: application/json

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
```

#### 3. Create Work Order
```bash
POST /api/tools/create_work_order
Content-Type: application/json

{
  "equipment_id": "HVAC-001",
  "root_cause": "Clogged air filter",
  "severity": "medium",
  "resolution_steps": ["Turn off system", "Replace filter"],
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
```

#### 4. Check Inventory
```bash
POST /api/tools/check_inventory
Content-Type: application/json

{
  "required_parts": [
    {
      "part_number": "FILTER-001",
      "name": "Air Filter",
      "quantity": 1,
      "cost": "$45"
    }
  ]
}
```

### Agent Endpoints

#### 1. Telemetry Agent
```bash
POST /api/agents/telemetry
Content-Type: application/json

{
  "equipment_id": "HVAC-001",
  "sensor_data": {
    "temperature": 88,
    "pressure": 42
  }
}
```

#### 2. Diagnostic Agent
```bash
POST /api/agents/diagnostic
Content-Type: application/json

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
```

#### 3. Orchestrator Agent
```bash
POST /api/agents/orchestrator
Content-Type: application/json

{
  "diagnosis": {
    "equipment_id": "HVAC-001",
    "root_cause": "Clogged air filter",
    "severity": "medium",
    "resolution_steps": ["Turn off system", "Replace filter"],
    "required_parts": [
      {
        "part_number": "FILTER-001",
        "quantity": 1,
        "cost": "$45"
      }
    ],
    "estimated_cost": "$45.00"
  }
}
```

### Workflow Endpoint

#### Run Complete Workflow
```bash
POST /api/workflow/run
Content-Type: application/json

{
  "equipment_id": "HVAC-001",
  "sensor_data": {
    "temperature": 88,
    "pressure": 42
  },
  "use_ai": false,
  "use_pinecone": false
}
```

**Response:**
```json
{
  "success": true,
  "workflow_complete": true,
  "steps": [
    {
      "step": 1,
      "agent": "telemetry_listener_agent",
      "action": "anomaly_detection",
      "result": {...}
    },
    {
      "step": 2,
      "agent": "diagnostic_expert_agent",
      "action": "diagnosis_generation",
      "result": {...}
    },
    {
      "step": 3,
      "agent": "orchestrator_agent",
      "action": "inventory_check",
      "result": {...}
    },
    {
      "step": 4,
      "agent": "orchestrator_agent",
      "action": "work_order_creation",
      "result": {...}
    }
  ],
  "summary": {
    "anomaly_detected": true,
    "anomaly_type": "overheating",
    "severity": "medium",
    "work_order_id": "WO-1000",
    "estimated_cost": "$45.00"
  }
}
```

### Work Order Management

#### Get All Work Orders
```bash
GET /api/work_orders
```

#### Get Specific Work Order
```bash
GET /api/work_orders/WO-1000
```

## 🧪 Testing with cURL

### Test Complete Workflow
```bash
curl -X POST http://localhost:8787/api/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "HVAC-001",
    "sensor_data": {
      "temperature": 88,
      "pressure": 42
    },
    "use_ai": false
  }'
```

### Test Anomaly Detection
```bash
curl -X POST http://localhost:8787/api/tools/detect_anomaly \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "HVAC-001",
    "sensor_data": {
      "temperature": 88,
      "pressure": 42
    }
  }'
```

### Check Health
```bash
curl http://localhost:8787/health
```

## 🔄 Integration with Dashboard

The mock API is designed to work seamlessly with the Streamlit dashboard:

```python
import requests

# Run workflow
response = requests.post(
    'http://localhost:8787/api/workflow/run',
    json={
        'equipment_id': 'HVAC-001',
        'sensor_data': {'temperature': 88, 'pressure': 42},
        'use_ai': False
    }
)

result = response.json()
print(f"Work Order: {result['summary']['work_order_id']}")
```

## 📊 Mock Data

The API uses the same mock data as the standalone Python system:

- **Equipment**: HVAC-001, HVAC-002, MOTOR-001, MOTOR-002
- **Inventory**: Pre-populated with common parts
- **Work Orders**: Stored in memory (resets on restart)

## 🔧 Configuration

### Port
Default: `8787`

To change port in [`app.py`](app.py):
```python
app.run(debug=True, host='0.0.0.0', port=8787)
```

### Debug Mode
Enabled by default for development. Disable for production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 🚦 Status Codes

- `200` - Success
- `400` - Bad Request (missing required fields)
- `404` - Not Found (work order doesn't exist)
- `500` - Internal Server Error

## 📝 Notes

- Work orders are stored in memory and will be lost when the server restarts
- The API uses the same core logic as `agents.py` for consistency
- All endpoints return JSON responses
- CORS is not enabled by default (add `flask-cors` if needed for web clients)

## 🔗 Related Files

- `../agents.py` - Standalone Python implementation
- `../data.py` - Sensor data and anomaly detection
- `../diagnosis.py` - Diagnostic engine
- `../orchestrate/` - watsonx Orchestrate implementation

## 🎯 Next Steps

1. Start the mock API server
2. Test endpoints with cURL or Postman
3. Integrate with Streamlit dashboard
4. Replace with actual watsonx Orchestrate when ready