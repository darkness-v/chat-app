#!/bin/bash

echo "🚀 Setting up Image Chat Feature..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Install backend dependencies
echo -e "${BLUE}📦 Installing backend dependencies...${NC}"

cd storage-service
echo -e "${YELLOW}Installing storage service dependencies...${NC}"
pip install -r requirements.txt
cd ..

cd chat-service
echo -e "${YELLOW}Installing chat service dependencies...${NC}"
pip install -r requirements.txt
cd ..

# 2. Create uploads directory
echo -e "${BLUE}📁 Creating uploads directory...${NC}"
mkdir -p storage-service/uploads
echo "Uploads directory created"

# 3. Run database migration (if DB exists)
echo -e "${BLUE}🗄️  Checking database migration...${NC}"
if [ -f "storage-service/chat.db" ]; then
    cd storage-service
    python migrate_db.py
    cd ..
else
    echo "No existing database found. Will be created with new schema."
fi

# 4. Install frontend dependencies
echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Node modules already installed, skipping..."
fi
cd ..

# 5. Check environment variables
echo -e "${BLUE}🔑 Checking environment variables...${NC}"
if [ ! -f "chat-service/.env" ]; then
    echo -e "${YELLOW}Warning: chat-service/.env not found${NC}"
    echo "Creating from example..."
    if [ -f "chat-service/.env.example" ]; then
        cp chat-service/.env.example chat-service/.env
        echo -e "${YELLOW}Please edit chat-service/.env and add your OPENAI_API_KEY${NC}"
    else
        echo "OPENAI_API_KEY=your_api_key_here" > chat-service/.env
        echo "STORAGE_SERVICE_URL=http://localhost:8002" >> chat-service/.env
        echo "MODEL=gpt-4o" >> chat-service/.env
        echo -e "${YELLOW}Created chat-service/.env - Please add your OPENAI_API_KEY${NC}"
    fi
else
    echo -e "${GREEN}✓ Environment file exists${NC}"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}To start the application, run these commands in separate terminals:${NC}"
echo ""
echo -e "  ${YELLOW}Terminal 1 - Storage Service:${NC}"
echo "    cd storage-service && python main.py"
echo ""
echo -e "  ${YELLOW}Terminal 2 - Chat Service:${NC}"
echo "    cd chat-service && python main.py"
echo ""
echo -e "  ${YELLOW}Terminal 3 - Frontend:${NC}"
echo "    cd frontend && npm run dev"
echo ""
echo -e "${BLUE}Then open http://localhost:3000${NC}"
echo ""
echo -e "${GREEN}📸 New Feature: Click the image icon to upload and chat with images!${NC}"
