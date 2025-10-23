#!/bin/bash
# Install seaborn library for correlation heatmaps

echo "🔧 Installing seaborn for correlation matrix visualizations..."

cd "$(dirname "$0")/chat-service"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "📦 Using UV package manager..."
    uv pip install seaborn>=0.12.0
else
    echo "📦 Using pip..."
    pip install seaborn>=0.12.0
fi

echo "✅ Seaborn installed successfully!"
echo ""
echo "Please restart the chat-service for changes to take effect:"
echo "  ./stop-services.sh"
echo "  ./start-services.sh"
