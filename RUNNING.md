# Chat Application - Currently Running! 🚀

## Services Status

All services are successfully running:

✅ **Storage Service** - Running on http://localhost:8002
- Handles conversation persistence
- SQLite database for storing chat history
- RESTful API for CRUD operations

✅ **Chat Service** - Running on http://localhost:8001  
- Handles AI chat logic with OpenAI
- Streaming responses support
- Communicates with Storage Service

✅ **Frontend** - Running on http://localhost:3000
- Next.js React application
- Modern, responsive UI
- Real-time streaming chat interface

## Access the Application

Open your browser and navigate to:
**http://localhost:3000**

## Features Implemented

### ✅ Multi-turn Conversation
- Persistent chat history across sessions
- All messages saved to database

### ✅ Message Display
- Shows who said what (User vs Assistant)
- Timestamps for each message
- Clean, modern UI

### ✅ Streaming & Loading States
- Real-time streaming of AI responses
- Loading indicators while waiting
- Smooth user experience

## Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js (Port 3000)
│   (React)       │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Chat Service   │  FastAPI (Port 8001)
│   (Python)      │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐      ┌─────────────┐
│ Storage Service │◄────►│   SQLite    │
│   (Python)      │      │   Database  │
└─────────────────┘      └─────────────┘
    FastAPI (Port 8002)
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Fetch API with streaming

### Backend Services
- **Framework**: FastAPI (Python)
- **Package Manager**: uv
- **Database**: SQLite with SQLAlchemy ORM
- **AI/LLM**: OpenAI API
- **Async HTTP**: httpx

### Infrastructure
- **Microservice Architecture**: 3 independent services
- **Communication**: REST APIs with JSON
- **Streaming**: Server-Sent Events (SSE)

## How to Use

1. **Start a New Conversation**
   - Click "New Conversation" button
   - Enter a title for your conversation

2. **Send Messages**
   - Type your message in the input box
   - Press Enter or click Send
   - Watch the AI response stream in real-time

3. **View History**
   - Select any conversation from the sidebar
   - See full conversation history
   - Continue conversations anytime

## API Endpoints

### Storage Service (Port 8002)
- `GET /health` - Health check
- `POST /api/conversations` - Create conversation
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/{id}` - Get conversation with messages
- `POST /api/conversations/{id}/messages` - Add message
- `DELETE /api/conversations/{id}` - Delete conversation

### Chat Service (Port 8001)
- `GET /health` - Health check
- `POST /api/chat` - Send message (non-streaming)
- `POST /api/chat/stream` - Send message (streaming)

## Database Location

SQLite database file: `storage-service/conversations.db`

## Environment Variables

### Chat Service (.env)
```
OPENAI_API_KEY=your-api-key-here
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o-mini
```

### Frontend (.env.local)
```
NEXT_PUBLIC_CHAT_SERVICE_URL=http://localhost:8001
```

## Stopping the Services

To stop any service, press `Ctrl+C` in its terminal window.

## Next Steps / Potential Enhancements

- [ ] Add user authentication
- [ ] Support for multiple AI models
- [ ] Message editing and deletion
- [ ] Export conversations
- [ ] Search across conversations
- [ ] Support for images and files
- [ ] Deploy to cloud (Docker containers ready)
- [ ] Add Redis for caching
- [ ] WebSocket for real-time updates

## Troubleshooting

If services don't start:
1. Check if ports 3000, 8001, 8002 are available
2. Verify OpenAI API key is set correctly
3. Ensure all dependencies are installed
4. Check service logs for errors

Enjoy your lightweight chat application! 🎉
