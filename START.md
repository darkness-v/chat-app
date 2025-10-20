# Chat Application - Start Guide

## Quick Start (Local Development)

### Method 1: Using Docker Compose (Recommended)

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

2. Run the application:
```bash
docker-compose up
```

3. Open http://localhost:3000

### Method 2: Manual Setup

1. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

2. Start each service in separate terminals:

**Terminal 1 - Storage Service:**
```bash
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002
```

**Terminal 2 - Chat Service:**
```bash
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

4. Open http://localhost:3000

## Service URLs

- Frontend: http://localhost:3000
- Chat Service: http://localhost:8001
- Storage Service: http://localhost:8002

## Testing the APIs

### Storage Service
```bash
curl -X POST http://localhost:8002/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Chat"}'

curl http://localhost:8002/api/conversations

curl -X POST http://localhost:8002/api/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "Hello!"}'

curl http://localhost:8002/api/conversations/1/messages
```

### Chat Service
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1, "message": "Hello!"}'
```

## Configuration

### Chat Service (.env)
- `OPENAI_API_KEY`: Your OpenAI API key
- `STORAGE_SERVICE_URL`: URL of storage service (default: http://localhost:8002)
- `MODEL`: OpenAI model to use (default: gpt-3.5-turbo)

### Frontend (.env.local)
- `NEXT_PUBLIC_CHAT_SERVICE_URL`: URL of chat service (default: http://localhost:8001)
- `NEXT_PUBLIC_STORAGE_SERVICE_URL`: URL of storage service (default: http://localhost:8002)

## Troubleshooting

### Port already in use
If ports 3000, 8001, or 8002 are already in use, you can change them:
- Frontend: Edit `frontend/package.json` scripts
- Chat Service: Edit port in `chat-service/main.py`
- Storage Service: Edit port in `storage-service/main.py`

### Database not persisting
Make sure the `storage-service` directory has write permissions for creating `chat_history.db`

### OpenAI API errors
- Verify your API key is correct in `chat-service/.env`
- Check your OpenAI account has credits
- Ensure you have access to the model specified (gpt-3.5-turbo by default)
