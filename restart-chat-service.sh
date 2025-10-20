#!/bin/bash

# Quick restart script for chat service after code changes

echo "🔄 Restarting Chat Service"
echo "=========================="
echo ""

# Find and kill chat service on port 8001
CHAT_PID=$(lsof -ti:8001)
if [ ! -z "$CHAT_PID" ]; then
    echo "📦 Stopping current chat service (PID: $CHAT_PID)..."
    kill $CHAT_PID
    sleep 2
    echo "✅ Stopped"
else
    echo "ℹ️  No chat service running on port 8001"
fi

echo ""
echo "🚀 Starting chat service with updated code..."

# Create logs directory if it doesn't exist
mkdir -p logs

cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001 > ../logs/chat-service.log 2>&1 &
CHAT_PID=$!

echo "✅ Chat service started (PID: $CHAT_PID)"
echo ""
echo "📊 Service running at: http://localhost:8001"
echo "📝 Logs: tail -f logs/chat-service.log"
echo ""
echo "🎉 Ready to test image chat!"
echo ""
