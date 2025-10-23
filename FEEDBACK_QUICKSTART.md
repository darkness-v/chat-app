# Like/Dislike Feedback - Quick Start

## Installation (One Command)

```bash
cd /Users/tani/TechJDI/chat-app
./setup-feedback-feature.sh
```

Then restart your services.

## What You Get

- 👍 Like button on assistant messages
- 👎 Dislike button on assistant messages  
- Feedback persists in database
- Smooth hover animations

## Test It

1. Start services: `./start-services.sh`
2. Open: http://localhost:3000
3. Send a message to the assistant
4. Hover over the assistant's response
5. Click 👍 or 👎
6. Refresh page - feedback persists!

## Files Changed

**Backend:**
- `storage-service/models.py` - Added feedback column
- `storage-service/schemas.py` - Added feedback field
- `storage-service/main.py` - Added PATCH endpoint
- `storage-service/add_feedback_column.py` - Migration script

**Frontend:**
- `frontend/src/types/index.ts` - Added feedback type
- `frontend/src/components/ChatMessage.tsx` - Added UI buttons
- `frontend/src/app/page.tsx` - Added handleFeedback function

## Architecture

```
User clicks 👍/👎
     ↓
ChatMessage.tsx (UI)
     ↓
page.tsx handleFeedback()
     ↓
PATCH /api/messages/{id}/feedback
     ↓
Database updated
     ↓
UI reflects change
```

## Query Feedback

```python
import sqlite3
conn = sqlite3.connect('storage-service/chat.db')
cursor = conn.cursor()

# Count likes and dislikes
cursor.execute("SELECT feedback, COUNT(*) FROM messages WHERE feedback IS NOT NULL GROUP BY feedback")
print(cursor.fetchall())
```

## Need Help?

Read the full guide: `FEEDBACK_FEATURE.md`
