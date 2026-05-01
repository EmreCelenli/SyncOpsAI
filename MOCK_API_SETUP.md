# Mock API Setup Guide

This guide explains how to set up and use the mock API servers for the hackathon demo.

## Overview

Since the hackathon doesn't have real Work Order, Inventory, or Technician Management Systems, we've created Flask-based mock APIs that simulate these systems. Agent 3 (Orchestrator) calls these APIs to complete the workflow.

## Architecture

```
Agent 3 (Orchestrator)
    ↓
watson_orchestrate_integration.py
    ↓
Mock API Servers (Flask)
    ├── Work Order API (port 5001)
    ├── Inventory API (port 5002)
    └── Technician API (port 5003)
```

## Mock API Servers

### 1. Work Order API (Port 5001)

**Endpoints:**
- `POST /api/v1/work-orders` - Create new work order
- `GET /api/v1/work-orders/<id>` - Get work order details
- `PATCH /api/v1/work-orders/<id>` - Update work order status
- `GET /api/v1/work-orders` - List all work orders

**Example Request:**
```bash
curl -X POST http://localhost:5001/api/v1/work-orders \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": "HVAC-001",
    "description": "Clogged air filter causing overheating",
    "parts_needed": ["Air Filter AF-2024"],
    "priority": "high"
  }'
```

### 2. Inventory API (Port 5002)

**Endpoints:**
- `POST /api/v1/inventory/check` - Check parts availability
- `POST /api/v1/inventory/reserve` - Reserve parts for work order
- `GET /api/v1/inventory/parts/<part>` - Get part details

**Example Request:**
```bash
curl -X POST http://localhost:5002/api/v1/inventory/check \
  -H "Content-Type: application/json" \
  -d '{
    "parts": ["Air Filter AF-2024", "Bearing RB-500"]
  }'
```

### 3. Technician API (Port 5003)

**Endpoints:**
- `POST /api/v1/technicians/find` - Find available technician
- `POST /api/v1/technicians/assign` - Assign technician to work order
- `GET /api/v1/technicians/<id>` - Get technician details
- `GET /api/v1/technicians` - List all technicians

**Example Request:**
```bash
curl -X POST http://localhost:5003/api/v1/technicians/find \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_type": "hvac",
    "priority": "high",
    "location": "Zone A"
  }'
```

## Starting the Mock APIs

### Option 1: Start All Servers (Recommended)

```bash
# Make script executable (first time only)
chmod +x mock_apis/start_all.sh

# Start all 3 servers
./mock_apis/start_all.sh
```

This will:
- Start Work Order API on port 5001
- Start Inventory API on port 5002
- Start Technician API on port 5003
- Create logs in `logs/` directory
- Display health check status

### Option 2: Start Individually

```bash
# Terminal 1 - Work Order API
python3 mock_apis/work_order_api.py

# Terminal 2 - Inventory API
python3 mock_apis/inventory_api.py

# Terminal 3 - Technician API
python3 mock_apis/technician_api.py
```

## Stopping the Mock APIs

```bash
# Stop all servers
./mock_apis/stop_all.sh

# Or manually kill processes
lsof -ti:5001 | xargs kill -9  # Work Order API
lsof -ti:5002 | xargs kill -9  # Inventory API
lsof -ti:5003 | xargs kill -9  # Technician API
```

## Health Checks

Each API has a health endpoint:

```bash
curl http://localhost:5001/health  # Work Order API
curl http://localhost:5002/health  # Inventory API
curl http://localhost:5003/health  # Technician API
```

## Integration with Agent 3

Agent 3 uses `watson_orchestrate_integration.py` which:

1. **First tries Watson Orchestrate** (if configured with API keys)
2. **Falls back to Mock APIs** (calls localhost:5001-5003)
3. **Ultimate fallback** (hardcoded responses if APIs unavailable)

This graceful degradation ensures the demo works even if:
- Watson Orchestrate is not configured
- Mock APIs are not running
- Network issues occur

## Mock Data

### Available Parts (Inventory)
- Air Filter AF-2024 ($45) - 15 units
- Bearing RB-500 ($120) - 8 units
- Compressor Seal Kit CS-2024 ($85) - 5 units
- Refrigerant R-410A ($120) - 20 units
- Motor Belt MB-100 ($35) - 12 units
- Thermostat TH-500 ($75) - 10 units

### Available Technicians
- TECH-001: John Smith (HVAC, Senior)
- TECH-002: Sarah Johnson (Motors, Senior)
- TECH-003: Mike Chen (HVAC, Intermediate)
- TECH-004: Emily Davis (Motors, Expert)

## Testing the Integration

1. **Start Mock APIs:**
   ```bash
   ./mock_apis/start_all.sh
   ```

2. **Run the POC system:**
   ```bash
   python -m poc.main
   ```

3. **Watch Agent 3 in action:**
   - Agent 1 detects anomaly
   - Agent 2 diagnoses issue
   - Agent 3 calls Mock APIs:
     - Creates work order
     - Checks inventory
     - Assigns technician

4. **View logs:**
   ```bash
   tail -f logs/work_order_api.log
   tail -f logs/inventory_api.log
   tail -f logs/technician_api.log
   ```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port
lsof -ti:5001 | xargs kill -9
```

### Flask Not Installed
```bash
pip install flask
# Or reinstall all requirements
pip install -r poc/requirements.txt
```

### APIs Not Responding
1. Check if servers are running: `ps aux | grep python`
2. Check logs in `logs/` directory
3. Verify ports are not blocked by firewall
4. Try restarting: `./mock_apis/stop_all.sh && ./mock_apis/start_all.sh`

## Demo Tips

1. **Start APIs before POC**: Ensure all 3 mock APIs are running before starting the main system
2. **Monitor logs**: Keep log terminals open to see API calls in real-time
3. **Show graceful degradation**: Stop APIs mid-demo to show fallback behavior
4. **Explain architecture**: Use this as opportunity to explain microservices architecture

## Next Steps

For production deployment:
1. Replace mock APIs with real enterprise systems
2. Configure Watson Orchestrate with real API keys
3. Add authentication/authorization to API endpoints
4. Implement proper error handling and retry logic
5. Add monitoring and alerting