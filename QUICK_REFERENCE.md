# Chat App - Quick Reference

## 🚀 Quick Start

```bash
# One-command setup
./setup-uv.sh

# Add your OpenAI API key
nano chat-service/.env

# Start all services
./start-services.sh

# Open browser
open http://localhost:3000
```

## 🛑 Stop Services

```bash
./stop-services.sh
```

## 📋 Manual Commands

### Setup
```bash
# Storage Service
cd storage-service && uv venv && uv pip install -e .

# Chat Service  
cd chat-service && uv venv && uv pip install -e .

# Frontend
cd frontend && npm install
```

### Run Services
```bash
# Storage (Terminal 1)
cd storage-service
uv run uvicorn main:app --port 8002

# Chat (Terminal 2)
cd chat-service
uv run uvicorn main:app --port 8001

# Frontend (Terminal 3)
cd frontend
npm run dev
```

## 🔧 Configuration

### chat-service/.env
```env
OPENAI_API_KEY=sk-...
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o-mini
```

### frontend/.env.local
```env
NEXT_PUBLIC_CHAT_SERVICE_URL=http://localhost:8001
NEXT_PUBLIC_STORAGE_SERVICE_URL=http://localhost:8002
```

## 📸 Image Chat

1. Click 📷 icon to upload image (PNG/JPG/JPEG)
2. Preview appears with × to remove
3. Type message or leave blank
4. Click Send
5. AI analyzes with GPT-4 Vision

## 🔍 Troubleshooting

### Ports in use
```bash
# Check ports
lsof -ti:8001  # Chat service
lsof -ti:8002  # Storage service
lsof -ti:3000  # Frontend

# Kill process
kill $(lsof -ti:8001)
```

### View logs
```bash
tail -f logs/storage-service.log
tail -f logs/chat-service.log
tail -f logs/frontend.log
```

### Reset database
```bash
cd storage-service
rm chat_history.db  # or chat.db
uv run uvicorn main:app --port 8002  # Recreates DB
```

### Fix database schema (missing image_url)
```bash
./fix-database.sh
```

### Reinstall dependencies
```bash
# Storage service
cd storage-service
rm -rf .venv
uv venv && uv pip install -e .

# Chat service
cd chat-service
rm -rf .venv
uv venv && uv pip install -e .

# Frontend
cd frontend
rm -rf node_modules
npm install
```

## 📚 File Locations

- **Images**: `storage-service/uploads/`
- **Database**: `storage-service/chat.db`
- **Logs**: `logs/`
- **Config**: `.env` files

## 🌐 URLs

- Frontend: http://localhost:3000
- Chat API: http://localhost:8001
- Storage API: http://localhost:8002
- API Docs: 
  - http://localhost:8001/docs
  - http://localhost:8002/docs

## 🔑 API Keys

### OpenAI
Get your API key: https://platform.openai.com/api-keys

Models used:
- Text: `gpt-4o-mini` (fast, cheap)
- Vision: `gpt-4o` (images)

## 💡 Tips

- Use `uv run` instead of activating venv
- Images stored locally in uploads/
- Conversations persist in SQLite DB
- Streaming enabled by default
- Images included in conversation history

## 📖 Documentation

- [README.md](./README.md) - Full documentation
- [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md) - Image features
- [UV_PACKAGE_MANAGER.md](./UV_PACKAGE_MANAGER.md) - UV guide
