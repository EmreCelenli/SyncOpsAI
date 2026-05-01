#!/bin/bash

# Start all mock API servers for hackathon demo
# Each server runs on a different port

echo "🚀 Starting Mock API Servers for Hackathon Demo"
echo "================================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing..."
    pip install flask
fi

# Kill any existing processes on these ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:5002 | xargs kill -9 2>/dev/null || true
lsof -ti:5003 | xargs kill -9 2>/dev/null || true

sleep 2

# Start Work Order API (port 5001)
echo ""
echo "📋 Starting Work Order API on port 5001..."
python3 mock_apis/work_order_api.py > logs/work_order_api.log 2>&1 &
WORK_ORDER_PID=$!
echo "   PID: $WORK_ORDER_PID"

sleep 2

# Start Inventory API (port 5002)
echo ""
echo "📦 Starting Inventory API on port 5002..."
python3 mock_apis/inventory_api.py > logs/inventory_api.log 2>&1 &
INVENTORY_PID=$!
echo "   PID: $INVENTORY_PID"

sleep 2

# Start Technician API (port 5003)
echo ""
echo "👷 Starting Technician API on port 5003..."
python3 mock_apis/technician_api.py > logs/technician_api.log 2>&1 &
TECHNICIAN_PID=$!
echo "   PID: $TECHNICIAN_PID"

sleep 3

# Check if all servers are running
echo ""
echo "🔍 Checking server health..."
echo ""

check_health() {
    local url=$1
    local name=$2
    if curl -s "$url" > /dev/null 2>&1; then
        echo "✅ $name is healthy"
        return 0
    else
        echo "❌ $name failed to start"
        return 1
    fi
}

check_health "http://localhost:5001/health" "Work Order API"
check_health "http://localhost:5002/health" "Inventory API"
check_health "http://localhost:5003/health" "Technician API"

echo ""
echo "================================================"
echo "✨ All Mock APIs are running!"
echo ""
echo "📋 Work Order API:   http://localhost:5001"
echo "📦 Inventory API:    http://localhost:5002"
echo "👷 Technician API:   http://localhost:5003"
echo ""
echo "📝 Logs are in logs/ directory"
echo ""
echo "To stop all servers, run: ./mock_apis/stop_all.sh"
echo "Or press Ctrl+C and run: kill $WORK_ORDER_PID $INVENTORY_PID $TECHNICIAN_PID"
echo ""

# Keep script running
wait

# Made with Bob
