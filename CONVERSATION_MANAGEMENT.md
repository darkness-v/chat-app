# Conversation Management Feature

## Overview
This feature adds ChatGPT-like conversation management to your chat application, allowing users to:
- Create multiple conversations
- Switch between conversations
- Delete old conversations
- Auto-generate conversation titles from the first message
- View conversations in a sidebar with timestamps

## What Was Added

### 1. Backend Changes (Storage Service)

#### New API Endpoint
- **PATCH `/api/conversations/{id}`** - Update conversation title
  ```json
  {
    "title": "New conversation title"
  }
  ```

#### New Schema
- `ConversationUpdate` in `schemas.py` - For partial conversation updates

### 2. Frontend Changes

#### New Component: Sidebar
**Location:** `frontend/src/components/Sidebar.tsx`

Features:
- Lists all conversations sorted by most recent
- "New Chat" button to create new conversations
- Click conversation to load it
- Delete button (hover to reveal)
- Responsive design (collapsible on mobile)
- Shows relative timestamps (e.g., "2 minutes ago")
- Mobile toggle button for small screens

#### Updated Main Page
**Location:** `frontend/src/app/page.tsx`

New State Management:
```typescript
const [conversations, setConversations] = useState<Conversation[]>([]);
const [sidebarOpen, setSidebarOpen] = useState(false);
const firstMessageSentRef = useRef(false);
```

New Functions:
- `loadConversations()` - Load all conversations on mount
- `createNewConversation()` - Create a new conversation
- `loadConversation(id)` - Switch to a different conversation
- `deleteConversation(id)` - Delete a conversation
- `updateConversationTitle(id, title)` - Update conversation title

Auto-title Generation:
- First user message automatically becomes conversation title (truncated to 50 chars)
- Works for both regular chat and CSV analysis mode

### 3. UI/UX Improvements

#### Layout
```
┌──────────────────────────────────────────┐
│ [Sidebar]    │  [Main Chat Area]         │
│              │                            │
│ + New Chat   │  ┌─ Chat Header ─┐        │
│              │  │                │        │
│ ○ Conv 1     │  │  Messages...   │        │
│ • Conv 2     │  │  Messages...   │        │
│ ○ Conv 3     │  │                │        │
│              │  └─ Input Box ────┘        │
└──────────────────────────────────────────┘
```

#### Responsive Design
- Desktop: Sidebar always visible
- Mobile: Sidebar hidden by default, toggle button in top-left
- Overlay background when sidebar open on mobile

#### Visual Indicators
- Current conversation highlighted in sidebar
- Hover effects on conversation items
- Delete button appears on hover
- Relative timestamps for each conversation

## How to Use

### Creating a New Conversation
1. Click the **"+ New Chat"** button in the sidebar
2. The app creates a new conversation and clears the chat area
3. Start chatting - first message becomes the title

### Switching Conversations
1. Click any conversation in the sidebar
2. The app loads all messages from that conversation
3. Continue chatting in the selected conversation

### Deleting Conversations
1. Hover over a conversation in the sidebar
2. Click the trash icon that appears
3. Confirm deletion
4. If you delete the current conversation, a new one is created automatically

### Mobile Usage
1. Click the menu icon (☰) in top-left to open sidebar
2. Select/create conversation
3. Sidebar auto-closes after selection

## Technical Details

### Data Flow

1. **On App Load:**
   ```
   loadConversations() 
   → Fetch all conversations
   → Load most recent conversation
   → Display messages
   ```

2. **On Send Message:**
   ```
   handleSendMessage()
   → Save user message
   → Stream AI response
   → If first message: updateConversationTitle()
   → Save assistant message
   ```

3. **On Create New:**
   ```
   createNewConversation()
   → POST /api/conversations
   → Clear current state
   → Set new conversation ID
   ```

### State Management

The app maintains several synchronized states:
- `conversations[]` - List of all conversations
- `conversationId` - Currently active conversation
- `messages[]` - Messages in current conversation
- `csvMode` - Whether current conversation is in CSV mode

When switching conversations:
- Messages are loaded from database
- CSV mode is reset (unless conversation has CSV data)
- Scroll position resets to bottom

### Title Generation

```typescript
if (!firstMessageSentRef.current && content.trim()) {
  firstMessageSentRef.current = true;
  const title = content.trim().slice(0, 50) + (content.length > 50 ? '...' : '');
  await updateConversationTitle(conversationId, title);
}
```

- Uses `useRef` to track if title has been set
- Takes first 50 characters of first message
- Adds "..." if message is longer
- Updates both backend and local state

## API Reference

### Storage Service Endpoints

#### List Conversations
```
GET /api/conversations
```
Response:
```json
[
  {
    "id": 1,
    "title": "What is machine learning?",
    "created_at": "2025-10-23T10:00:00Z",
    "updated_at": "2025-10-23T10:05:00Z"
  }
]
```

#### Create Conversation
```
POST /api/conversations
Content-Type: application/json

{
  "title": "New Conversation"
}
```

#### Update Conversation
```
PATCH /api/conversations/{id}
Content-Type: application/json

{
  "title": "Updated title"
}
```

#### Delete Conversation
```
DELETE /api/conversations/{id}
```

#### Get Conversation with Messages
```
GET /api/conversations/{id}
```

## Testing

### Test Scenario 1: Basic Conversation Flow
1. Start the app
2. Send a message "Hello, how are you?"
3. Check sidebar - conversation title should be "Hello, how are you?"
4. Click "+ New Chat"
5. Send "Tell me about Python"
6. Check sidebar - should show both conversations
7. Click first conversation
8. Verify previous messages are loaded

### Test Scenario 2: CSV Analysis Mode
1. Create new conversation
2. Upload a CSV file
3. Ask "Summarize the data"
4. Title should be "Summarize the data"
5. Create new conversation
6. Verify CSV mode is disabled in new conversation
7. Return to CSV conversation
8. Verify CSV mode persists (Note: Currently resets - enhancement opportunity)

### Test Scenario 3: Mobile Responsiveness
1. Resize browser to mobile width (< 768px)
2. Verify sidebar is hidden
3. Click menu button (☰)
4. Verify sidebar slides in with overlay
5. Click a conversation
6. Verify sidebar closes automatically

### Test Scenario 4: Deletion
1. Create 3 conversations
2. Delete the middle one
3. Verify it's removed from sidebar
4. Delete the current conversation
5. Verify app creates a new conversation automatically

## Known Limitations & Future Enhancements

### Current Limitations
1. CSV mode doesn't persist when switching conversations
2. No search/filter for conversations
3. No conversation rename functionality
4. No conversation export/import
5. Timestamps don't update in real-time

### Potential Enhancements
1. **Search/Filter:** Add search bar to filter conversations
2. **Folders/Tags:** Organize conversations into categories
3. **Rename:** Double-click title to edit
4. **Pin Conversations:** Pin important conversations to top
5. **Archive:** Archive old conversations instead of deleting
6. **Export:** Export conversation as Markdown/PDF
7. **Share:** Generate shareable links
8. **Conversation Metadata:** Track tokens used, model used, etc.
9. **CSV Persistence:** Remember CSV files associated with conversations
10. **Infinite Scroll:** Load conversations on-demand for large lists

## Troubleshooting

### Sidebar not showing on desktop
- Check browser width is > 768px
- Check CSS classes in Sidebar.tsx
- Verify `sidebarOpen` state in dev tools

### Conversations not loading
- Check browser console for API errors
- Verify storage service is running on port 8002
- Check database file exists and has read/write permissions

### Title not updating
- Verify first message contains text
- Check `firstMessageSentRef` is resetting on conversation switch
- Verify PATCH endpoint is working (check network tab)

### Messages from wrong conversation
- Verify `conversationId` state is correct
- Check `loadConversation()` is awaiting properly
- Ensure messages are filtered by conversation_id in backend

## Migration Notes

If you have existing data:
- Existing conversations will work without changes
- Existing messages will be preserved
- May want to update titles of old conversations manually
- Database schema is backward compatible

## Performance Considerations

- Conversations are loaded once on mount, then cached
- Message loading happens on conversation switch (network call)
- Consider pagination for users with 100+ conversations
- Consider virtualization for very long message histories

## Accessibility

Current accessibility features:
- Keyboard navigation works in sidebar
- Focus states on interactive elements
- Semantic HTML structure

Future improvements:
- ARIA labels for screen readers
- Keyboard shortcuts (Ctrl+N for new chat, etc.)
- Focus management when switching conversations
- Announce conversation changes to screen readers

## Summary

This feature transforms the single-conversation chat app into a full multi-conversation system similar to ChatGPT. Users can now:
- Manage multiple conversations simultaneously
- Easily switch between different topics
- Keep their chat history organized
- Access past conversations anytime

The implementation is clean, maintainable, and ready for future enhancements!
