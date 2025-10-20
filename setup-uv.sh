#!/bin/bash

# Chat Application Setup Script with UV
# This script sets up the entire chat application with image support

set -e  # Exit on error

echo "🚀 Setting up Chat Application with Image Support"
echo "=================================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ UV installed successfully"
    echo "⚠️  Please restart your terminal and run this script again"
    exit 0
fi

echo "✅ UV is installed"
echo ""

# Setup Storage Service
echo "📦 Setting up Storage Service..."
cd storage-service

# Create virtual environment and install dependencies with uv
echo "  - Creating virtual environment with uv..."
uv venv

echo "  - Installing dependencies..."
uv pip install -r requirements.txt

# Create uploads directory
echo "  - Creating uploads directory..."
mkdir -p uploads
touch uploads/.gitkeep

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "  - Creating .env file..."
    cat > .env << EOF
# Storage Service Configuration
DATABASE_URL=sqlite:///./chat.db
EOF
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

cd ..
echo "✅ Storage Service setup complete"
echo ""

# Setup Chat Service
echo "💬 Setting up Chat Service..."
cd chat-service

# Create virtual environment and install dependencies with uv
echo "  - Creating virtual environment with uv..."
uv venv

echo "  - Installing dependencies..."
uv pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "  - Creating .env file..."
    cat > .env << EOF
# Chat Service Configuration
OPENAI_API_KEY=your_api_key_here
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o-mini
EOF
    echo "✅ Created .env file"
    echo "⚠️  Please update .env with your OpenAI API key!"
else
    echo "✅ .env file already exists"
fi

cd ..
echo "✅ Chat Service setup complete"
echo ""

# Setup Frontend
echo "🎨 Setting up Frontend..."
cd frontend

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "  - Installing Node.js dependencies..."
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "✅ Node.js dependencies already installed"
fi

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "  - Creating .env.local file..."
    cat > .env.local << EOF
# Frontend Configuration
NEXT_PUBLIC_CHAT_SERVICE_URL=http://localhost:8001
NEXT_PUBLIC_STORAGE_SERVICE_URL=http://localhost:8002
EOF
    echo "✅ Created .env.local file"
else
    echo "✅ .env.local file already exists"
fi

cd ..
echo "✅ Frontend setup complete"
echo ""

# Database migration (if database exists)
echo "🗄️  Checking database migration..."
cd storage-service
if [ -f "chat_history.db" ] || [ -f "chat.db" ]; then
    echo "  - Running migration to add image_url column..."
    uv run python migrate_db.py
else
    echo "  - No existing database found. Will create with new schema on first run."
fi
cd ..
echo ""

echo "✅ Setup Complete!"
echo ""
echo "=================================================="
echo "🎉 All services are ready!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Update chat-service/.env with your OpenAI API key"
echo "2. Run the services:"
echo ""
echo "   Terminal 1 - Storage Service:"
echo "   cd storage-service && uv run uvicorn main:app --host 0.0.0.0 --port 8002"
echo ""
echo "   Terminal 2 - Chat Service:"
echo "   cd chat-service && uv run uvicorn main:app --host 0.0.0.0 --port 8001"
echo ""
echo "   Terminal 3 - Frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see IMAGE_CHAT_GUIDE.md"
echo ""
