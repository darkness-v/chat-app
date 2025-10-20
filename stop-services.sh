#!/bin/bash

# Stop all chat application services

echo "🛑 Stopping Chat Application Services"
echo "======================================"
echo ""

# Read PIDs from file if it exists
if [ -f .service-pids ]; then
    source .service-pids
    
    if [ ! -z "$STORAGE_PID" ]; then
        echo "📦 Stopping Storage Service (PID: $STORAGE_PID)..."
        kill $STORAGE_PID 2>/dev/null && echo "   ✅ Stopped" || echo "   ⚠️  Already stopped or not found"
    fi
    
    if [ ! -z "$CHAT_PID" ]; then
        echo "💬 Stopping Chat Service (PID: $CHAT_PID)..."
        kill $CHAT_PID 2>/dev/null && echo "   ✅ Stopped" || echo "   ⚠️  Already stopped or not found"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "🎨 Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null && echo "   ✅ Stopped" || echo "   ⚠️  Already stopped or not found"
    fi
    
    rm .service-pids
else
    echo "⚠️  No .service-pids file found"
    echo "   Attempting to stop by port..."
    
    # Try to kill by port
    STORAGE_PID=$(lsof -ti:8002)
    if [ ! -z "$STORAGE_PID" ]; then
        echo "📦 Stopping Storage Service on port 8002..."
        kill $STORAGE_PID 2>/dev/null && echo "   ✅ Stopped"
    fi
    
    CHAT_PID=$(lsof -ti:8001)
    if [ ! -z "$CHAT_PID" ]; then
        echo "💬 Stopping Chat Service on port 8001..."
        kill $CHAT_PID 2>/dev/null && echo "   ✅ Stopped"
    fi
    
    FRONTEND_PID=$(lsof -ti:3000)
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "🎨 Stopping Frontend on port 3000..."
        kill $FRONTEND_PID 2>/dev/null && echo "   ✅ Stopped"
    fi
fi

echo ""
echo "✅ All services stopped"
echo ""
