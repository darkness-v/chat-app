#!/bin/bash

# Setup script for CSV Data Analysis feature

echo "🔧 Setting up CSV Data Analysis feature..."

# Navigate to chat-service
cd "$(dirname "$0")/chat-service" || exit 1

echo "📦 Installing Python dependencies..."
if command -v uv &> /dev/null; then
    echo "Using UV package manager..."
    uv pip install pandas numpy matplotlib
else
    echo "Using pip..."
    pip install pandas numpy matplotlib
fi

echo "✅ Dependencies installed!"
echo ""
echo "📋 New Files Created:"
echo "  - chat-service/code_executor.py"
echo "  - chat-service/data_analysis_agent.py"
echo "  - frontend/src/components/CSVUpload.tsx"
echo "  - CSV_ANALYSIS_GUIDE.md"
echo ""
echo "🔄 New API Endpoints:"
echo "  - POST /api/csv-analysis/stream"
echo "  - POST /api/csv-analysis/clear/{conversation_id}"
echo "  - GET /api/csv-analysis/dataframes/{conversation_id}"
echo "  - POST /api/upload-csv (storage-service)"
echo ""
echo "🚀 To start using CSV analysis:"
echo "  1. Restart services: ./stop-services.sh && ./start-services.sh"
echo "  2. Open http://localhost:3000"
echo "  3. Upload a CSV file or provide URL"
echo "  4. Ask questions about your data!"
echo ""
echo "📖 Read CSV_ANALYSIS_GUIDE.md for detailed documentation"
