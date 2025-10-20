# 🎨 Chat App - Visual Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                    http://localhost:3000                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Frontend (Next.js + React)                         │    │
│  │  • Chat UI                                          │    │
│  │  • Image Upload Button 📷                          │    │
│  │  • Image Preview                                    │    │
│  │  • Message Display                                  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
         │                              │
         │ HTTP/REST                    │ Image Upload
         │                              │
         ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Chat Service        │      │  Storage Service     │
│  :8001               │◄─────┤  :8002               │
│                      │      │                      │
│  • OpenAI API        │      │  • SQLite DB         │
│  • Vision Support    │      │  • Image Storage     │
│  • Streaming         │      │  • File Upload       │
│  • Context Mgmt      │      │  • Static Files      │
└──────────────────────┘      └──────────────────────┘
         │                              │
         │                              │
         ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  OpenAI API          │      │  Local Storage       │
│  • gpt-4o-mini       │      │  • chat.db           │
│  • gpt-4o (vision)   │      │  • uploads/          │
└──────────────────────┘      └──────────────────────┘
```

## 🔄 Image Chat Flow

```
1. User Action                    2. Upload
┌──────────────┐                 ┌──────────────┐
│  Click 📷    │                 │ POST /upload │
│  Select PNG  │────────────────►│   -image     │
│  or JPG      │                 │              │
└──────────────┘                 └──────────────┘
                                         │
                                         ▼
3. Preview                        4. Save URL
┌──────────────┐                 ┌──────────────┐
│  [IMAGE]     │                 │ /uploads/    │
│  [× Remove]  │◄────────────────│ uuid.jpg     │
│              │                 │              │
└──────────────┘                 └──────────────┘
       │
       │ User types message
       │ (or leaves blank)
       ▼
5. Send Message
┌──────────────────────────────────────┐
│ POST /api/chat/stream                │
│ {                                    │
│   message: "What's in this image?"   │
│   image_url: "/uploads/uuid.jpg"     │
│   conversation_id: 1                 │
│ }                                    │
└──────────────────────────────────────┘
       │
       ▼
6. Chat Service
┌──────────────────────────────────────┐
│ • Fetch conversation history         │
│ • Format for Vision API:             │
│   - Text messages as text            │
│   - Image messages as vision format  │
│ • Call OpenAI with gpt-4o            │
└──────────────────────────────────────┘
       │
       ▼
7. Stream Response
┌──────────────────────────────────────┐
│ data: {"content": "I", "done": false}│
│ data: {"content": " see", ...}       │
│ data: {"content": " a", ...}         │
│ data: {"content": "", "done": true}  │
└──────────────────────────────────────┘
       │
       ▼
8. Display in Chat
┌──────────────────────────────────────┐
│ 👤 You · 10:30                       │
│ ┌──────────────────────────────┐    │
│ │ [IMAGE PREVIEW]              │    │
│ │ What's in this image?        │    │
│ └──────────────────────────────┘    │
│                                      │
│ 🤖 Assistant · 10:30                 │
│ ┌──────────────────────────────┐    │
│ │ I see a beautiful sunset...   │    │
│ └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

## 📁 File Structure

```
chat-app/
│
├── 🚀 Setup & Control
│   ├── setup-uv.sh           # One-time setup
│   ├── start-services.sh     # Start everything
│   └── stop-services.sh      # Stop everything
│
├── 📚 Documentation
│   ├── README.md                 # Main docs
│   ├── IMAGE_CHAT_GUIDE.md       # Image features
│   ├── UV_PACKAGE_MANAGER.md     # UV guide
│   ├── QUICK_REFERENCE.md        # Quick commands
│   └── IMPLEMENTATION_SUMMARY.md # This implementation
│
├── 📦 Storage Service (Port 8002)
│   ├── main.py                # FastAPI app
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # DB connection
│   ├── pyproject.toml         # UV config
│   ├── requirements.txt       # Fallback deps
│   ├── migrate_db.py          # DB migration
│   └── uploads/               # 🖼️ Images stored here
│
├── 💬 Chat Service (Port 8001)
│   ├── main.py                # FastAPI app + Vision
│   ├── pyproject.toml         # UV config
│   ├── requirements.txt       # Fallback deps
│   └── .env                   # 🔑 OpenAI API key
│
└── 🎨 Frontend (Port 3000)
    ├── src/
    │   ├── app/
    │   │   └── page.tsx       # Main chat page
    │   ├── components/
    │   │   ├── ChatInput.tsx  # 📷 Upload UI
    │   │   └── ChatMessage.tsx# 🖼️ Display images
    │   └── types/
    │       └── index.ts       # TypeScript types
    └── package.json
```

## 🎯 Component Breakdown

### ChatInput Component
```
┌─────────────────────────────────────────────┐
│  [Preview: Remove ×]                        │
│  ┌───────┬──────────────────────┬────────┐ │
│  │  📷   │ Type message...      │ [Send] │ │
│  │       │                      │        │ │
│  └───────┴──────────────────────┴────────┘ │
└─────────────────────────────────────────────┘
```

Features:
- 📷 Click to upload
- 👁️ Preview with × to remove
- ⌨️ Enter to send, Shift+Enter for new line
- 🚫 Disabled state during loading

### ChatMessage Component
```
User Message:
┌────────────────────────────────────┐
│ 👤 You · 10:30                     │
│ ┌────────────────────────────┐    │
│ │ [IMAGE]                    │    │
│ │ Describe this image        │    │
│ └────────────────────────────┘    │
└────────────────────────────────────┘

Assistant Message:
┌────────────────────────────────────┐
│ 🤖 Assistant · 10:30               │
│ ┌────────────────────────────┐    │
│ │ I see a landscape with...  │    │
│ └────────────────────────────┘    │
└────────────────────────────────────┘
```

## 🔄 State Management

```
Frontend State:
├── conversationId: number
├── messages: Message[]
├── isLoading: boolean
├── isStreaming: boolean
└── imageFile: File | null

Message Type:
├── id: number
├── conversation_id: number
├── role: 'user' | 'assistant'
├── content: string
├── image_url?: string      ← New!
└── timestamp: string
```

## 🛠️ UV Workflow

```
Setup Phase:
┌──────────────┐
│ uv venv      │ → Create virtual environment
├──────────────┤
│ uv pip       │ → Install dependencies
│ install -e . │    from pyproject.toml
└──────────────┘

Development Phase:
┌──────────────┐
│ uv run       │ → Run any Python command
│ uvicorn ...  │    in the virtual environment
└──────────────┘
   No activation needed! ✨
```

## 📊 API Request/Response

### Upload Image
```
Request:
POST /api/upload-image
Content-Type: multipart/form-data

file: [binary image data]

Response:
{
  "image_url": "/uploads/550e8400-e29b-41d4-a716-446655440000.jpg"
}
```

### Send Message with Image
```
Request:
POST /api/chat/stream
Content-Type: application/json

{
  "conversation_id": 1,
  "message": "What's in this image?",
  "image_url": "/uploads/550e8400...jpg"
}

Response (SSE Stream):
data: {"content": "I", "done": false}

data: {"content": " see", "done": false}

data: {"content": " a", "done": false}

data: {"content": "", "done": true}
```

## 💾 Database Schema

```sql
conversations
├── id (PK)
├── title
├── created_at
└── updated_at

messages
├── id (PK)
├── conversation_id (FK)
├── role
├── content
├── image_url        ← New!
└── timestamp
```

## 🎓 Quick Commands Cheat Sheet

```bash
# Setup (once)
./setup-uv.sh

# Start
./start-services.sh

# Stop
./stop-services.sh

# View logs
tail -f logs/chat-service.log

# Check ports
lsof -ti:8001 :8002 :3000

# Reset database
rm storage-service/chat.db

# Reinstall deps
cd storage-service && uv pip install -e .
```

## 🎉 Success Indicators

✅ All ports listening (8001, 8002, 3000)
✅ Frontend opens without errors
✅ Can send text messages
✅ Can upload and preview images
✅ Image messages show in history
✅ AI responds to image questions
✅ Conversation persists on refresh

Happy chatting! 🚀
