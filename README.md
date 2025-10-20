# Lightweight Multi-Turn Chat Application

A microservice-based chat application with persistent conversation history and streaming support.

## Architecture

### Services
1. **Chat Service** (Port 8001) - Handles AI chat interactions and streaming
2. **Storage Service** (Port 8002) - Manages conversation persistence
3. **Frontend Service** (Port 3000) - React/Next.js UI

## Features
- ✅ Multi-turn conversation history
- ✅ Message persistence with timestamps
- ✅ Streaming responses with loading states
- ✅ User/Assistant message differentiation
- ✅ Clean, modern UI

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js, React, Tailwind CSS
- **AI**: OpenAI API (configurable)

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key

### Backend Setup

1. Install dependencies for Chat Service:
```bash
cd chat-service
pip install -r requirements.txt
```

2. Install dependencies for Storage Service:
```bash
cd storage-service
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
OPENAI_API_KEY=your_api_key_here
STORAGE_SERVICE_URL=http://localhost:8002
```

4. Run services:
```bash
cd storage-service
python main.py

cd chat-service
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Open http://localhost:3000
2. Start chatting!
3. Your conversation history is automatically saved

## API Endpoints

### Chat Service (8001)
- `POST /api/chat/stream` - Stream chat responses
- `GET /health` - Health check

### Storage Service (8002)
- `POST /api/conversations` - Create conversation
- `GET /api/conversations/{id}` - Get conversation
- `POST /api/conversations/{id}/messages` - Add message
- `GET /api/conversations/{id}/messages` - Get messages
- `GET /health` - Health check
