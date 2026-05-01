#!/bin/bash

# SyncOpsAI - watsonx Orchestrate Import Script
# This script imports all agents and tools into watsonx Orchestrate

set -e  # Exit on error

echo "=========================================="
echo "SyncOpsAI - watsonx Orchestrate Import"
echo "=========================================="
echo ""

# Check if orchestrate CLI is installed
if ! command -v orchestrate &> /dev/null; then
    echo "ERROR: orchestrate CLI not found"
    echo "Please install: pip install ibm-watsonx-orchestrate"
    exit 1
fi

# Check if logged in
echo "Checking authentication..."
if ! orchestrate auth status &> /dev/null; then
    echo "ERROR: Not authenticated with watsonx Orchestrate"
    echo "Please run: orchestrate auth login"
    exit 1
fi

echo "✓ Authentication verified"
echo ""

# Import Tools
echo "=========================================="
echo "Importing Tools"
echo "=========================================="
echo ""

echo "1. Importing detect_anomaly tool..."
orchestrate tools import -k python -f tools/detect_anomaly.py
echo "✓ detect_anomaly imported"
echo ""

echo "2. Importing generate_diagnosis tool..."
orchestrate tools import -k python -f tools/generate_diagnosis.py
echo "✓ generate_diagnosis imported"
echo ""

echo "3. Importing create_work_order tool..."
orchestrate tools import -k python -f tools/create_work_order.py
echo "✓ create_work_order imported"
echo ""

echo "4. Importing check_inventory tool..."
orchestrate tools import -k python -f tools/check_inventory.py
echo "✓ check_inventory imported"
echo ""

# Import Agents
echo "=========================================="
echo "Importing Agents"
echo "=========================================="
echo ""

echo "1. Importing Telemetry Listener Agent..."
orchestrate agents import -f agents/telemetry_agent.yaml
echo "✓ telemetry_listener_agent imported"
echo ""

echo "2. Importing Diagnostic Expert Agent..."
orchestrate agents import -f agents/diagnostic_agent.yaml
echo "✓ diagnostic_expert_agent imported"
echo ""

echo "3. Importing Orchestrator Agent..."
orchestrate agents import -f agents/orchestrator_agent.yaml
echo "✓ orchestrator_agent imported"
echo ""

# Summary
echo "=========================================="
echo "Import Complete!"
echo "=========================================="
echo ""
echo "Imported Components:"
echo "  Tools: 4"
echo "    - detect_anomaly"
echo "    - generate_diagnosis"
echo "    - create_work_order"
echo "    - check_inventory"
echo ""
echo "  Agents: 3"
echo "    - telemetry_listener_agent"
echo "    - diagnostic_expert_agent"
echo "    - orchestrator_agent"
echo ""
echo "Next Steps:"
echo "  1. Verify imports: orchestrate agents list"
echo "  2. Test agents in watsonx Orchestrate UI"
echo "  3. Configure agent collaborations"
echo ""
echo "=========================================="

# Made with Bob
