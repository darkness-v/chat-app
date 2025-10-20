#!/bin/bash

# Quick Start Script for Chat Application
# Uses UV for Python environment management

set -e

echo "🚀 Starting Chat Application Services"
echo "======================================"
echo ""

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    fi
    return 0
}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please run ./setup-uv.sh first"
    exit 1
fi

# Check ports
echo "🔍 Checking if ports are available..."
check_port 8001 || echo "   Chat Service port 8001 may be in use"
check_port 8002 || echo "   Storage Service port 8002 may be in use"
check_port 3000 || echo "   Frontend port 3000 may be in use"
echo ""

# Check if setup has been run
if [ ! -d "storage-service/.venv" ] || [ ! -d "chat-service/.venv" ]; then
    echo "❌ Virtual environments not found. Please run ./setup-uv.sh first"
    exit 1
fi

# Check for OpenAI API key
if ! grep -q "sk-" chat-service/.env 2>/dev/null; then
    echo "⚠️  OpenAI API key not found in chat-service/.env"
    echo "   Please add your API key before starting the services"
    echo ""
fi

echo "Starting services in background..."
echo ""

# Create logs directory
mkdir -p logs

# Start Storage Service
echo "📦 Starting Storage Service on port 8002..."
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002 > ../logs/storage-service.log 2>&1 &
STORAGE_PID=$!
echo "   PID: $STORAGE_PID"
cd ..

# Wait a bit for storage service to start
sleep 2

# Start Chat Service
echo "💬 Starting Chat Service on port 8001..."
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001 > ../logs/chat-service.log 2>&1 &
CHAT_PID=$!
echo "   PID: $CHAT_PID"
cd ..

# Wait a bit for chat service to start
sleep 2

# Start Frontend
echo "🎨 Starting Frontend on port 3000..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   PID: $FRONTEND_PID"
cd ..

# Save PIDs to file for easy stopping
cat > .service-pids << EOF
STORAGE_PID=$STORAGE_PID
CHAT_PID=$CHAT_PID
FRONTEND_PID=$FRONTEND_PID
EOF

echo ""
echo "✅ All services started!"
echo ""
echo "======================================"
echo "📊 Service Status:"
echo "======================================"
echo "Storage Service:  http://localhost:8002 (PID: $STORAGE_PID)"
echo "Chat Service:     http://localhost:8001 (PID: $CHAT_PID)"
echo "Frontend:         http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "📝 Logs are being written to the logs/ directory"
echo ""
echo "To view logs:"
echo "  tail -f logs/storage-service.log"
echo "  tail -f logs/chat-service.log"
echo "  tail -f logs/frontend.log"
echo ""
echo "To stop all services:"
echo "  ./stop-services.sh"
echo ""
echo "🎉 Open http://localhost:3000 to use the chat application!"
echo ""
