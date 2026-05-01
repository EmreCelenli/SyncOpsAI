# Watson Orchestrate Setup Guide

## Overview

This guide explains how to set up and deploy the Work Order Orchestrator agent in Watson Orchestrate for Agent 3 of the SyncOps AI system.

## Prerequisites

- Watson Orchestrate account and workspace
- API keys for:
  - Work Order Management System
  - Inventory Management System
  - Technician Management System

## Files Created

### Agent Definition
- `agents/work_order_orchestrator.yaml` - Main agent configuration with skills and workflow

### Tool Definitions
- `tools/work_order_api.yaml` - Work Order Management System API
- `tools/inventory_api.yaml` - Inventory Management System API
- `tools/technician_api.yaml` - Technician Management System API

## Deployment Steps

### 1. Configure Environment Variables

Add these to your `.env` file or Watson Orchestrate environment:

```bash
# Work Order System
WORK_ORDER_API_URL=https://your-work-order-system.com
WORK_ORDER_API_KEY=your_api_key_here

# Inventory System
INVENTORY_API_URL=https://your-inventory-system.com
INVENTORY_API_KEY=your_api_key_here

# Technician System
TECHNICIAN_API_URL=https://your-technician-system.com
TECHNICIAN_API_KEY=your_api_key_here
```

### 2. Deploy Tools to Watson Orchestrate

```bash
# Deploy Work Order API tool
watson-orchestrate tools deploy tools/work_order_api.yaml

# Deploy Inventory API tool
watson-orchestrate tools deploy tools/inventory_api.yaml

# Deploy Technician API tool
watson-orchestrate tools deploy tools/technician_api.yaml
```

### 3. Deploy Agent

```bash
# Deploy the Work Order Orchestrator agent
watson-orchestrate agents deploy agents/work_order_orchestrator.yaml
```

### 4. Test the Agent

```bash
# Test work order creation
watson-orchestrate agents test work_order_orchestrator \
  --skill create_work_order \
  --params '{
    "equipment_id": "HVAC-001",
    "issue_description": "Clogged air filter causing overheating",
    "required_parts": ["Air Filter AF-2024"],
    "priority": "high"
  }'
```

## Agent Skills

### 1. Create Work Order
Creates a maintenance work order in the work order management system.

**Input:**
- `equipment_id` (string, required): Equipment identifier
- `issue_description` (string, required): Root cause diagnosis
- `required_parts` (array, required): List of parts needed
- `priority` (string, optional): Priority level (low/medium/high/critical)

**Output:**
- `work_order_id`: Unique work order identifier
- `status`: Work order status
- `assigned_to`: Assigned technician (if auto-assigned)
- `estimated_completion`: Estimated completion time

### 2. Check Inventory
Checks parts availability in the inventory system.

**Input:**
- `parts` (array, required): List of part numbers to check

**Output:**
- `all_available`: Boolean indicating if all parts are available
- `parts_status`: Detailed status for each part
- `backorder_items`: List of parts on backorder
- `estimated_delivery`: Delivery date for backorder items

### 3. Assign Technician
Auto-assigns a technician based on skills and availability.

**Input:**
- `work_order_id` (string, required): Work order identifier
- `required_skills` (array, required): Required technician skills
- `priority` (string, optional): Assignment priority

**Output:**
- `technician_id`: Assigned technician ID
- `technician_name`: Technician name
- `estimated_arrival`: Estimated arrival time
- `status`: Assignment status

## Workflow

The agent follows this automated workflow:

1. **Create Work Order** → Creates WO in system
2. **Check Inventory** → Verifies parts availability
3. **Assign Technician** → Auto-assigns based on skills
4. **Notify Complete** → Returns results to calling system

If parts are unavailable, the workflow logs the backorder and continues with technician assignment.

## Integration with SyncOps AI

The Python integration (`watson_orchestrate_integration.py`) calls this agent through the Watson Orchestrate API:

```python
from watson_orchestrate_integration import get_watson_orchestrate

orchestrate = get_watson_orchestrate()

# Create work order
result = orchestrate.create_work_order(
    equipment_id="HVAC-001",
    diagnosis="Clogged air filter causing overheating",
    parts_needed=["Air Filter AF-2024"],
    priority="high"
)
```

## Monitoring

The agent includes built-in monitoring for:
- Work orders created
- Average response time
- Parts availability rate
- Technician assignment rate

Access metrics through Watson Orchestrate dashboard.

## Troubleshooting

### Agent Not Found
```bash
# List deployed agents
watson-orchestrate agents list

# Redeploy if needed
watson-orchestrate agents deploy agents/work_order_orchestrator.yaml
```

### API Connection Errors
- Verify API URLs and keys in environment variables
- Check API endpoint availability
- Review Watson Orchestrate logs

### Skill Execution Failures
- Check tool configurations in `tools/` directory
- Verify API response schemas match tool definitions
- Review agent workflow in `agents/work_order_orchestrator.yaml`

## Next Steps

1. Configure your actual API endpoints
2. Deploy tools and agent to Watson Orchestrate
3. Test each skill individually
4. Run end-to-end workflow test
5. Integrate with SyncOps AI POC

## Support

For Watson Orchestrate specific issues:
- Documentation: https://www.ibm.com/docs/en/watson-orchestrate
- Support: https://www.ibm.com/mysupport

For SyncOps AI integration issues:
- See `QUICKSTART.md` for system setup
- Check `watson_orchestrate_integration.py` for API wrapper