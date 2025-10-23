# Like/Dislike Feedback Feature

## Overview

Your chat application now supports user feedback on assistant responses through like/dislike buttons, similar to ChatGPT. Users can click on thumbs up or thumbs down icons to provide feedback on the quality of AI responses.

## Features

✨ **Like/Dislike Buttons**: Each assistant message has feedback buttons
👍 **Thumbs Up**: Indicates the response was helpful
👎 **Thumbs Down**: Indicates the response needs improvement
🔄 **Toggle Feedback**: Click again to remove feedback
💾 **Persistent Storage**: Feedback is saved in the database
🎨 **Smooth UI**: Buttons appear on hover or stay visible when feedback is given
🎯 **Assistant Only**: Feedback buttons only appear on assistant messages

## Installation & Migration

### Step 1: Update Database Schema

Run the migration script to add the feedback column to your existing database:

```bash
cd /Users/tani/TechJDI/chat-app/storage-service
python add_feedback_column.py
```

Output should show:
```
🔄 Starting database migration...
Adding feedback column to messages table...
✅ Successfully added feedback column
✅ Migration complete!
```

### Step 2: Restart Services

After migration, restart your services to apply the changes:

```bash
cd /Users/tani/TechJDI/chat-app
./stop-services.sh
./start-services.sh
```

Or manually:

```bash
# Terminal 1 - Storage Service
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002

# Terminal 2 - Chat Service  
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001

# Terminal 3 - Frontend
cd frontend
npm run dev
```

## How It Works

### Database Layer

**New Column in `messages` table:**
- `feedback` (VARCHAR(20), nullable): Stores 'like', 'dislike', or NULL

### Backend API

**New Endpoint:**
```
PATCH /api/messages/{message_id}/feedback
```

**Request Body:**
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
  "content": "Here's the answer...",
  "timestamp": "2025-10-23T10:30:00Z",
  "feedback": "like"
}
```

**Validations:**
- Only assistant messages can receive feedback
- Feedback values must be: `"like"`, `"dislike"`, or `null`
- Invalid message IDs return 404

### Frontend UI

**Button Behavior:**
- Buttons appear on hover over assistant messages
- Once clicked, buttons stay visible with highlighted state
- Green highlight for "like", red highlight for "dislike"
- Click again to toggle off (remove feedback)

**Visual States:**
1. **Hidden**: Buttons are invisible until hover (when no feedback set)
2. **Visible on Hover**: Buttons appear with gray color
3. **Active (Liked)**: Green background with filled icon
4. **Active (Disliked)**: Red background with filled icon

## Usage Examples

### Test the Feature

1. **Start a conversation:**
   ```
   Open http://localhost:3000
   Send: "What is machine learning?"
   ```

2. **Give positive feedback:**
   - Hover over the assistant's response
   - Click the thumbs up button 👍
   - Button should turn green and stay visible

3. **Change feedback:**
   - Click the thumbs down button 👎
   - The thumbs up should deselect
   - Thumbs down should turn red

4. **Remove feedback:**
   - Click the active button again
   - Both buttons should return to gray/hidden state

5. **Verify persistence:**
   - Refresh the page
   - The feedback should persist on the message

### API Testing

Test the feedback endpoint directly:

```bash
# Like a message
curl -X PATCH http://localhost:8002/api/messages/1/feedback \
  -H "Content-Type: application/json" \
  -d '{"feedback":"like"}'

# Dislike a message
curl -X PATCH http://localhost:8002/api/messages/1/feedback \
  -H "Content-Type: application/json" \
  -d '{"feedback":"dislike"}'

# Remove feedback
curl -X PATCH http://localhost:8002/api/messages/1/feedback \
  -H "Content-Type: application/json" \
  -d '{"feedback":null}'

# Get message with feedback
curl http://localhost:8002/api/conversations/1
```

## Data Analysis

Query feedback statistics from your database:

```python
import sqlite3

conn = sqlite3.connect('chat.db')
cursor = conn.cursor()

# Count likes vs dislikes
cursor.execute("""
    SELECT 
        feedback, 
        COUNT(*) as count 
    FROM messages 
    WHERE feedback IS NOT NULL 
    GROUP BY feedback
""")
print("Feedback Statistics:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Get messages with negative feedback
cursor.execute("""
    SELECT id, content, feedback 
    FROM messages 
    WHERE feedback = 'dislike'
    LIMIT 10
""")
print("\nMessages with Dislike:")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1][:50]}...")

conn.close()
```

## File Changes Summary

### Backend Changes

1. **`storage-service/models.py`**
   - Added `feedback` column to Message model

2. **`storage-service/schemas.py`**
   - Added `feedback` field to MessageBase
   - Created `MessageFeedbackUpdate` schema

3. **`storage-service/main.py`**
   - Added `PATCH /api/messages/{message_id}/feedback` endpoint

4. **`storage-service/add_feedback_column.py`** (new)
   - Migration script for existing databases

### Frontend Changes

1. **`frontend/src/types/index.ts`**
   - Added `feedback` property to Message interface

2. **`frontend/src/components/ChatMessage.tsx`**
   - Added like/dislike button UI
   - Added hover state management
   - Added feedback toggle logic
   - Integrated Heroicons for thumbs up/down

3. **`frontend/src/app/page.tsx`**
   - Added `handleFeedback` function
   - Passed feedback handler to ChatMessage components

## Troubleshooting

### Buttons not appearing
- Check that you're hovering over an **assistant** message (not user message)
- Ensure browser JavaScript is enabled
- Check browser console for errors

### Feedback not persisting
- Verify storage-service is running on port 8002
- Check database has feedback column: `sqlite3 chat.db "PRAGMA table_info(messages)"`
- Verify API endpoint: `curl http://localhost:8002/api/messages/1/feedback`

### Migration fails
- Backup your database first: `cp chat.db chat.db.backup`
- Check if column already exists
- Try manual SQL: `sqlite3 chat.db "ALTER TABLE messages ADD COLUMN feedback VARCHAR(20)"`

### Styling issues
- Clear browser cache (Cmd+Shift+R / Ctrl+Shift+R)
- Check Tailwind CSS classes are compiling
- Verify Next.js dev server is running

## Future Enhancements

Potential improvements to consider:

1. **Feedback Reasons**: Add optional text input for why they liked/disliked
2. **Analytics Dashboard**: Show feedback statistics over time
3. **Feedback Filter**: Filter conversations by feedback type
4. **Export Feedback**: Export disliked messages for model improvement
5. **Feedback Notifications**: Notify when negative feedback is received
6. **Batch Feedback**: Allow rating multiple messages at once
7. **Star Ratings**: Expand to 5-star rating system
8. **Feedback Categories**: Categorize feedback (accuracy, helpfulness, tone, etc.)

## Success Checklist

✅ Database migration completed successfully  
✅ Services restarted  
✅ Like/dislike buttons appear on assistant messages  
✅ Buttons show on hover  
✅ Clicking like highlights green  
✅ Clicking dislike highlights red  
✅ Toggling feedback works (click again to remove)  
✅ Feedback persists after page refresh  
✅ User messages don't show feedback buttons  
✅ Mobile view works correctly  

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review server logs in `chat-app/logs/`
3. Check browser console for frontend errors
4. Verify all services are running: `ps aux | grep uvicorn`

Enjoy your new feedback feature! 🎉
