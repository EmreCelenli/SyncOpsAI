#!/bin/bash

# SyncOpsAI Dashboard Launcher
# Starts both Mock API and Streamlit Dashboard

echo "=========================================="
echo "SyncOpsAI Dashboard Launcher"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "Error: Please run this script from the dashboard directory"
    echo "Usage: cd dashboard && ./run_dashboard.sh"
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing dashboard dependencies..."
    pip install -r requirements.txt
fi

# Check if Mock API dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing Mock API dependencies..."
    pip install -r ../mock_apis/requirements.txt
fi

echo "✓ Dependencies installed"
echo ""

# Start Mock API in background
echo "Starting Mock API server..."
cd ../mock_apis
python app.py > /dev/null 2>&1 &
API_PID=$!
cd ../dashboard

# Wait for API to start
sleep 2

# Check if API is running
if curl -s http://localhost:8787/health > /dev/null; then
    echo "✓ Mock API running on http://localhost:8787 (PID: $API_PID)"
else
    echo "⚠️  Mock API may not have started correctly"
fi

echo ""
echo "Starting Streamlit Dashboard..."
echo "Dashboard will open at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=========================================="
echo ""

# Start Streamlit
streamlit run app.py

# Cleanup on exit
echo ""
echo "Stopping Mock API server..."
kill $API_PID 2>/dev/null
echo "✓ Servers stopped"

# Made with Bob
