#!/bin/bash

# Stop all mock API servers

echo "🛑 Stopping Mock API Servers..."
echo ""

# Kill processes on ports 5001, 5002, 5003
echo "Stopping Work Order API (port 5001)..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "   No process found"

echo "Stopping Inventory API (port 5002)..."
lsof -ti:5002 | xargs kill -9 2>/dev/null || echo "   No process found"

echo "Stopping Technician API (port 5003)..."
lsof -ti:5003 | xargs kill -9 2>/dev/null || echo "   No process found"

echo ""
echo "✅ All mock API servers stopped"

# Made with Bob
