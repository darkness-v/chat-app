#!/bin/bash

# Setup script for like/dislike feedback feature
# This script will migrate the database and restart services

echo "🚀 Setting up Like/Dislike Feedback Feature"
echo "=========================================="
echo ""

# Navigate to storage service directory
cd "$(dirname "$0")/storage-service"

# Run migration
echo "📊 Running database migration..."
python add_feedback_column.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration completed successfully!"
    echo ""
    echo "🔄 Now restart your services:"
    echo ""
    echo "  Option 1 - Use start script:"
    echo "  cd /Users/tani/TechJDI/chat-app"
    echo "  ./stop-services.sh"
    echo "  ./start-services.sh"
    echo ""
    echo "  Option 2 - Manual restart:"
    echo "  Terminal 1: cd storage-service && uv run uvicorn main:app --host 0.0.0.0 --port 8002"
    echo "  Terminal 2: cd chat-service && uv run uvicorn main:app --host 0.0.0.0 --port 8001"
    echo "  Terminal 3: cd frontend && npm run dev"
    echo ""
    echo "📖 Read FEEDBACK_FEATURE.md for full documentation"
    echo ""
else
    echo ""
    echo "❌ Migration failed. Please check the error messages above."
    exit 1
fi
