# Like/Dislike Feature - Visual Guide

## UI Preview

```
┌─────────────────────────────────────────────────────────┐
│  User Message                                           │
│  ┌──────────────────────────────────────┐              │
│  │ U │ "What is machine learning?"      │              │
│  └──────────────────────────────────────┘              │
│                                                          │
│  Assistant Message                                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ AI│ Machine learning is a subset of AI...       │  │
│  │   │ It involves training algorithms...          │  │
│  │   │                                              │  │
│  │   │ Assistant · 10:30                            │  │
│  │   │                                              │  │
│  │   │  👍    👎      ← Hover to reveal            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Button States

### State 1: Hidden (No Feedback Set)
```
┌────────────────────────┐
│ Assistant · 10:30      │
│                        │  ← Buttons hidden
└────────────────────────┘
```

### State 2: Visible on Hover
```
┌────────────────────────┐
│ Assistant · 10:30      │
│                        │
│ [👍] [👎]              │  ← Gray buttons appear
└────────────────────────┘
```

### State 3: Liked (Active)
```
┌────────────────────────┐
│ Assistant · 10:30      │
│                        │
│ [👍] [👎]              │  ← Green thumbs up
└────────────────────────┘
```

### State 4: Disliked (Active)
```
┌────────────────────────┐
│ Assistant · 10:30      │
│                        │
│ [👍] [👎]              │  ← Red thumbs down
└────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│   Browser    │
│ (User clicks │
│   like/      │
│  dislike)    │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  ChatMessage.tsx     │
│  - Handles UI state  │
│  - Shows/hides btns  │
│  - Updates visuals   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│    page.tsx          │
│  handleFeedback()    │
│  - Calls API         │
│  - Updates state     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Storage Service     │
│  PATCH /api/messages │
│  /{id}/feedback      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   SQLite Database    │
│   messages table     │
│   feedback column    │
└──────────────────────┘
```

## Database Schema

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER,
    role VARCHAR(50),
    content TEXT,
    image_url VARCHAR(500),
    plots JSON,
    timestamp DATETIME,
    feedback VARCHAR(20),  ← NEW!
    FOREIGN KEY (conversation_id) 
        REFERENCES conversations(id)
);
```

## API Endpoint

```
PATCH /api/messages/{message_id}/feedback
```

**Request:**
```json
{
  "feedback": "like"  // or "dislike" or null
}
```

**Response:**
```json
{
  "id": 123,
  "conversation_id": 1,
  "role": "assistant",
  "content": "Machine learning is...",
  "timestamp": "2025-10-23T10:30:00Z",
  "feedback": "like",  ← Updated!
  "image_url": null,
  "plots": null
}
```

## Component Structure

```
page.tsx
├── Sidebar
├── ChatInput
└── ChatMessage (for each message)
    ├── Avatar (AI/U)
    ├── Message Content
    ├── Timestamp
    └── Feedback Buttons (assistant only)
        ├── Like Button 👍
        └── Dislike Button 👎
```

## CSS Classes

```tsx
// Like button (active)
className="bg-green-100 text-green-600"

// Dislike button (active)  
className="bg-red-100 text-red-600"

// Buttons (inactive)
className="text-gray-400"

// Hover state
className="hover:bg-gray-200"
```

## User Journey

```
1. User sends message
   ↓
2. AI responds
   ↓
3. User hovers over AI message
   ↓
4. 👍 👎 buttons appear
   ↓
5. User clicks 👍
   ↓
6. Button turns green
   ↓
7. Feedback saved to DB
   ↓
8. User refreshes page
   ↓
9. 👍 still green (persisted!)
```

## Feature Highlights

✅ **ChatGPT-like UX** - Same behavior as popular AI chat apps
✅ **Smooth Animations** - Fade in/out on hover
✅ **Toggle Feedback** - Click again to remove
✅ **Persistent** - Saved in database
✅ **Mobile Ready** - Works on touch devices
✅ **Accessible** - Proper ARIA labels
✅ **User-Only** - No feedback on user messages

## Color Scheme

```
Like (Active):
  Background: #dcfce7 (green-100)
  Icon: #16a34a (green-600)

Dislike (Active):
  Background: #fee2e2 (red-100)  
  Icon: #dc2626 (red-600)

Inactive:
  Icon: #9ca3af (gray-400)
  Hover bg: #e5e7eb (gray-200)
```

## Testing Checklist

- [ ] Hover shows buttons
- [ ] Like button works
- [ ] Dislike button works
- [ ] Toggle removes feedback
- [ ] Feedback persists on refresh
- [ ] Mobile touch works
- [ ] No buttons on user messages
- [ ] Database saves correctly
- [ ] Multiple messages work independently
