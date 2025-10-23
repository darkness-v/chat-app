# Lightweight Multi-Turn Chat Application

A microservice-based chat application with persistent conversation history, streaming support, and **ChatGPT-like conversation management**.

## 🆕 NEW: Conversation Management (October 2025)
Your app now has a **sidebar with conversation list**! Just like ChatGPT, you can:
- 📝 Create multiple conversations
- 🔄 Switch between conversations
- 🗑️ Delete old conversations
- ✨ Auto-generated titles from first message
- 📱 Mobile-responsive sidebar

**[→ Quick Start Guide](./CONVERSATION_QUICKSTART.md)** | **[→ Full Documentation](./DOCS_INDEX_CONVERSATIONS.md)**

## Architecture

### Services
1. **Chat Service** (Port 8001) - Handles AI chat interactions, streaming, and vision API
2. **Storage Service** (Port 8002) - Manages conversation persistence and image uploads
3. **Frontend Service** (Port 3000) - React/Next.js UI with conversation sidebar

## Features
- ✅ **Multi-conversation management (NEW!)**
- ✅ **Conversation sidebar with list (NEW!)**
- ✅ **Auto-generated titles (NEW!)**
- ✅ Multi-turn conversation history
- ✅ Message persistence with timestamps
- ✅ Streaming responses with loading states
- ✅ User/Assistant message differentiation
- ✅ **Image upload and chat (PNG/JPG/JPEG)**
- ✅ **CSV data analysis with plots**
- ✅ **Image preview in conversation**
- ✅ **GPT-4 Vision integration**
- ✅ Clean, modern UI with responsive design

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, UV (package manager)
- **Frontend**: Next.js, React, Tailwind CSS
- **AI**: OpenAI API (GPT-4o for vision, GPT-4o-mini for text)

## Quick Start (Recommended)

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API Key
- UV (will be installed automatically)

### One-Command Setup

```bash
# Clone and navigate to the project
cd chat-app

# Run setup script (installs UV if needed)
./setup-uv.sh

# Update your OpenAI API key
nano chat-service/.env
# or
code chat-service/.env

# Start all services
./start-services.sh

# Open http://localhost:3000 in your browser
```

### Stop Services

```bash
./stop-services.sh
```

## Manual Setup

### Backend Setup with UV

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Storage Service**:
```bash
cd storage-service
uv venv
uv pip install -e .
mkdir -p uploads
```

3. **Chat Service**:
```bash
cd chat-service
uv venv
uv pip install -e .
```

4. **Set up environment variables**:

chat-service/.env:
```bash
OPENAI_API_KEY=your_api_key_here
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o-mini
```

5. **Run services**:
```bash
# Terminal 1 - Storage Service
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002

# Terminal 2 - Chat Service
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Open http://localhost:3000
2. **Text Chat**: Type a message and press Enter or click Send
3. **Image Chat**: 
   - Click the 📷 image icon to upload an image
   - Preview appears with × button to remove
   - Add a message or leave blank (defaults to "What is in this image?")
   - Click Send
   - AI analyzes the image using GPT-4 Vision
4. Images and messages appear in conversation history
5. All conversations are automatically saved

## Image Chat Features

- **Supported formats**: PNG, JPG, JPEG
- **Preview**: See your image before sending
- **Vision AI**: Powered by GPT-4o
- **Multi-turn**: Images are included in conversation context
- **Persistent**: Images stored locally in storage-service/uploads/

## API Endpoints

### Chat Service (8001)
- `POST /api/chat/stream` - Stream chat responses (supports image_url)
- `POST /api/chat` - Non-streaming endpoint
- `GET /health` - Health check

### Storage Service (8002)
- `POST /api/conversations` - Create conversation
- `GET /api/conversations/{id}` - Get conversation
- `POST /api/conversations/{id}/messages` - Add message (supports image_url)
- `GET /api/conversations/{id}/messages` - Get messages
- `POST /api/upload-image` - Upload image file
- `GET /uploads/{filename}` - Serve uploaded images
- `GET /health` - Health check

## Project Structure

```
chat-app/
├── setup-uv.sh              # Automated setup with UV
├── start-services.sh        # Start all services
├── stop-services.sh         # Stop all services
├── IMAGE_CHAT_GUIDE.md      # Detailed image chat documentation
├── storage-service/         # Persistence & image storage
│   ├── main.py
│   ├── models.py           # Added image_url field
│   ├── pyproject.toml      # UV configuration
│   ├── migrate_db.py       # Database migration
│   └── uploads/            # Uploaded images
├── chat-service/           # AI chat logic
│   ├── main.py            # Vision API support
│   └── pyproject.toml     # UV configuration
└── frontend/              # Next.js UI
    ├── src/
    │   ├── components/
    │   │   ├── ChatInput.tsx    # Image upload UI
    │   │   └── ChatMessage.tsx  # Image display
    │   └── app/
    │       └── page.tsx         # Main chat page
    └── package.json
```

## Environment Management with UV

This project uses [UV](https://github.com/astral-sh/uv) for fast, reliable Python package management:

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution
- **Simple**: Drop-in replacement for pip/venv

### UV Commands

```bash
# Install dependencies
uv pip install -e .

# Run Python scripts
uv run python script.py

# Run services
uv run uvicorn main:app --port 8001

# Add new dependency
uv pip install package-name
```

## Database Migration

If upgrading from a version without image support:

```bash
cd storage-service
uv run python migrate_db.py
```

## Troubleshooting

### Images not uploading
- Check `storage-service/uploads/` directory exists
- Verify `python-multipart` is installed: `uv pip list | grep multipart`

### Vision API errors
- Ensure using `gpt-4o` or `gpt-4o-mini` model
- Verify OpenAI API key has vision access
- Check image URL is accessible

### Services won't start
- Check ports 8001, 8002, 3000 are not in use
- View logs in `logs/` directory
- Verify `.env` files are configured

### UV issues
- Reinstall: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Update: `uv self update`

## Documentation

- [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md) - Detailed image chat documentation
- [UV_GUIDE.md](./UV_GUIDE.md) - UV package manager guide

## Cost Considerations

- **Text-only**: ~$0.15 per 1M tokens (gpt-4o-mini)
- **Vision**: ~$2.50 per 1M tokens + $0.001275 per image (gpt-4o)

Consider monitoring usage and setting limits.
