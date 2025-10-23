# Conversation Management Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌──────────────────────────────────────┐  │
│  │   Sidebar      │  │         Main Chat Area               │  │
│  │                │  │                                       │  │
│  │ + New Chat     │  │  ┌─────────────────────────────┐    │  │
│  │                │  │  │      Chat Header            │    │  │
│  │ Conversations: │  │  └─────────────────────────────┘    │  │
│  │  • Conv 1 [X]  │  │                                       │  │
│  │  • Conv 2 [X]  │  │  ┌─────────────────────────────┐    │  │
│  │  • Conv 3 [X]  │  │  │      Messages Area          │    │  │
│  │                │  │  │  - User messages            │    │  │
│  │                │  │  │  - Assistant messages       │    │  │
│  │                │  │  │  - Image previews           │    │  │
│  └────────────────┘  │  │  - CSV plots                │    │  │
│                      │  └─────────────────────────────┘    │  │
│                      │                                       │  │
│                      │  ┌─────────────────────────────┐    │  │
│                      │  │      Chat Input             │    │  │
│                      │  │  [Text] [Image] [CSV]       │    │  │
│                      │  └─────────────────────────────┘    │  │
│                      └──────────────────────────────────────┘  │
│                                                                  │
│  State Management:                                              │
│  • conversations[] - List of all conversations                  │
│  • conversationId - Current active conversation                 │
│  • messages[] - Messages in current conversation                │
│  • csvMode, csvPath - CSV analysis state                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                    HTTP/REST API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND SERVICES (FastAPI)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐        ┌──────────────────────────┐  │
│  │  Storage Service     │        │    Chat Service          │  │
│  │  Port: 8002          │        │    Port: 8001            │  │
│  │                      │        │                          │  │
│  │  Endpoints:          │        │  • OpenAI Integration   │  │
│  │  • GET  /api/        │        │  • Streaming Responses  │  │
│  │    conversations     │        │  • Image Chat (GPT-4o)  │  │
│  │  • POST /api/        │        │  • CSV Analysis         │  │
│  │    conversations     │        │  • Code Execution       │  │
│  │  • PATCH /api/       │        │                          │  │
│  │    conversations/:id │        │                          │  │
│  │  • DELETE /api/      │        │                          │  │
│  │    conversations/:id │        │                          │  │
│  │  • GET/POST /api/    │        │                          │  │
│  │    conversations/:id/│        │                          │  │
│  │    messages          │        │                          │  │
│  │  • POST /api/        │        │                          │  │
│  │    upload-image      │        │                          │  │
│  │  • POST /api/        │        │                          │  │
│  │    upload-csv        │        │                          │  │
│  └──────────────────────┘        └──────────────────────────┘  │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────────┐                                       │
│  │  SQLite Database     │                                       │
│  │                      │                                       │
│  │  Tables:             │                                       │
│  │  • conversations     │                                       │
│  │    - id              │                                       │
│  │    - title           │                                       │
│  │    - created_at      │                                       │
│  │    - updated_at      │                                       │
│  │                      │                                       │
│  │  • messages          │                                       │
│  │    - id              │                                       │
│  │    - conversation_id │                                       │
│  │    - role            │                                       │
│  │    - content         │                                       │
│  │    - image_url       │                                       │
│  │    - plots (JSON)    │                                       │
│  │    - timestamp       │                                       │
│  └──────────────────────┘                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. App Initialization Flow
```
User opens app
    ▼
loadConversations()
    ▼
GET /api/conversations
    ▼
Receive conversations[]
    ▼
Load most recent conversation
    ▼
loadConversation(id)
    ▼
GET /api/conversations/{id}/messages
    ▼
Display messages in UI
```

### 2. Create New Conversation Flow
```
User clicks "+ New Chat"
    ▼
createNewConversation()
    ▼
POST /api/conversations
    { title: "New Conversation" }
    ▼
Receive new conversation object
    ▼
Update conversations[] state
Set conversationId = new id
Clear messages[]
Reset CSV mode
    ▼
Ready for new chat
```

### 3. Send Message Flow
```
User types message & sends
    ▼
handleSendMessage()
    ▼
Check if first message
    ├─ Yes: Generate title from message
    │        ▼
    │   PATCH /api/conversations/{id}
    │        { title: "Message preview..." }
    │        ▼
    │   Update sidebar title
    │
    └─ No: Continue
    ▼
Add user message to UI
    ▼
POST /api/conversations/{id}/messages
    { role: "user", content: "..." }
    ▼
POST /api/chat/stream
    { conversation_id, message }
    ▼
Stream response chunks
    ▼
Update UI with streaming text
    ▼
POST /api/conversations/{id}/messages
    { role: "assistant", content: "..." }
    ▼
Complete
```

### 4. Switch Conversation Flow
```
User clicks conversation in sidebar
    ▼
loadConversation(id)
    ▼
Set conversationId = id
    ▼
GET /api/conversations/{id}/messages
    ▼
Clear current messages[]
    ▼
Load new messages[]
    ▼
Reset CSV mode
    ▼
Scroll to bottom
    ▼
Close sidebar (on mobile)
```

### 5. Delete Conversation Flow
```
User clicks delete icon
    ▼
Confirm deletion
    ▼
deleteConversation(id)
    ▼
DELETE /api/conversations/{id}
    ▼
Remove from conversations[] state
    ▼
Check if deleted current conversation
    ├─ Yes: Create new conversation
    │        ▼
    │   createNewConversation()
    │
    └─ No: Continue using current
```

## Component Hierarchy

```
page.tsx (Main App)
├── State Management
│   ├── conversations[]
│   ├── conversationId
│   ├── messages[]
│   ├── csvMode & csvPath
│   └── sidebarOpen
│
├── Functions
│   ├── loadConversations()
│   ├── createNewConversation()
│   ├── loadConversation(id)
│   ├── deleteConversation(id)
│   ├── updateConversationTitle(id, title)
│   ├── handleSendMessage()
│   └── handleSendCSVMessage()
│
└── Components
    ├── Sidebar
    │   ├── Props:
    │   │   ├── conversations
    │   │   ├── currentConversationId
    │   │   ├── onSelectConversation
    │   │   ├── onNewConversation
    │   │   ├── onDeleteConversation
    │   │   ├── isOpen
    │   │   └── onToggle
    │   └── Features:
    │       ├── Conversation list
    │       ├── New chat button
    │       ├── Delete buttons
    │       ├── Mobile toggle
    │       └── Timestamps
    │
    ├── CSVUpload (existing)
    │   └── Props: onUpload, disabled
    │
    ├── ChatMessage (existing)
    │   └── Props: message, plots
    │
    └── ChatInput (existing)
        └── Props: onSend, disabled
```

## API Contract

### Storage Service API

```typescript
// GET /api/conversations
Response: Conversation[]

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

// POST /api/conversations
Request: { title?: string }
Response: Conversation

// PATCH /api/conversations/{id}
Request: { title?: string }
Response: Conversation

// DELETE /api/conversations/{id}
Response: { message: string }

// GET /api/conversations/{id}/messages
Response: Message[]

interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  image_url?: string;
  plots?: string[];
  timestamp: string;
}
```

## State Synchronization

```
Frontend State          Database State
─────────────────       ──────────────
conversations[]    ←→   conversations table
conversationId     →    Current selection
messages[]         ←→   messages table (filtered)
csvMode            →    Derived from messages
csvPath            →    Temporary (not persisted)
```

## Key Design Decisions

1. **Auto-Title Generation**: First message becomes title
   - Simple and intuitive
   - No extra user input needed
   - Can be manually changed in future enhancement

2. **Sidebar Always Loads All Conversations**: 
   - Simple for small-medium usage
   - May need pagination for 100+ conversations
   - Easy to implement search/filter later

3. **CSV Mode Resets on Switch**:
   - Prevents confusion
   - Keeps code execution contexts clean
   - Can enhance to persist CSV context per conversation

4. **Responsive Design**:
   - Desktop: Sidebar always visible
   - Mobile: Collapsible with overlay
   - Consistent experience across devices

5. **Optimistic UI Updates**:
   - Title updates immediately in sidebar
   - No waiting for server confirmation
   - Better perceived performance

## Files Modified/Created

### New Files
- `frontend/src/components/Sidebar.tsx` - Sidebar component
- `CONVERSATION_MANAGEMENT.md` - Full documentation
- `CONVERSATION_QUICKSTART.md` - Quick start guide
- `CONVERSATION_ARCHITECTURE.md` - This file

### Modified Files
- `frontend/src/app/page.tsx` - Main app with conversation management
- `storage-service/main.py` - Added PATCH endpoint
- `storage-service/schemas.py` - Added ConversationUpdate schema

### Unchanged (Reused)
- `frontend/src/components/ChatMessage.tsx`
- `frontend/src/components/ChatInput.tsx`
- `frontend/src/components/CSVUpload.tsx`
- `frontend/src/types/index.ts` (used existing Conversation interface)
- Database models (fully compatible)

## Summary

This architecture provides:
✅ Clean separation of concerns  
✅ Scalable state management  
✅ RESTful API design  
✅ Responsive UI  
✅ Maintainable code structure  
✅ Easy to extend with new features  

The implementation follows React best practices and FastAPI patterns, making it easy for other developers to understand and extend.
