echo "🚀 Setting up Chat Application..."

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set!"
    echo "Please set it in chat-service/.env or export it:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key
    if [ -n "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
    fi
fi

echo "📝 Creating environment files..."

if [ ! -f "chat-service/.env" ]; then
    cp chat-service/.env.example chat-service/.env
    if [ -n "$OPENAI_API_KEY" ]; then
        echo "OPENAI_API_KEY=$OPENAI_API_KEY" > chat-service/.env
        echo "STORAGE_SERVICE_URL=http://localhost:8002" >> chat-service/.env
        echo "MODEL=gpt-5-mini" >> chat-service/.env
    fi
    echo "✅ Created chat-service/.env"
fi

if [ ! -f "frontend/.env.local" ]; then
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
fi

echo ""
echo "📦 Installing dependencies with uv..."

if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "Installing Storage Service dependencies..."
cd storage-service
uv pip install -r requirements.txt
cd ..

echo "Installing Chat Service dependencies..."
cd chat-service
uv pip install -r requirements.txt
cd ..

echo "Installing Frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Terminal 1: cd storage-service && uv run uvicorn main:app --host 0.0.0.0 --port 8002"
echo "2. Terminal 2: cd chat-service && uv run uvicorn main:app --host 0.0.0.0 --port 8001"
echo "3. Terminal 3: cd frontend && npm run dev"
echo ""
echo "Or use Docker Compose:"
echo "docker-compose up"
