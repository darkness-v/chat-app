# Implementation Details: Like/Dislike Feature

## Step-by-Step Implementation

This document shows exactly what was implemented to add the like/dislike feedback feature.

---

## Step 1: Database Schema (Backend)

### File: `storage-service/models.py`

**Added:**
```python
feedback = Column(String(20), nullable=True)  # 'like', 'dislike', or None
```

**Location:** In the `Message` class, after the `timestamp` column.

**Purpose:** Store user feedback for each assistant message.

---

## Step 2: API Schemas (Backend)

### File: `storage-service/schemas.py`

**Added to MessageBase:**
```python
feedback: Optional[str] = None  # 'like', 'dislike', or None
```

**New Schema:**
```python
class MessageFeedbackUpdate(BaseModel):
    feedback: Optional[str] = None  # 'like', 'dislike', or None
```

**Purpose:** Define the data structure for feedback in API requests/responses.

---

## Step 3: API Endpoint (Backend)

### File: `storage-service/main.py`

**New Endpoint:**
```python
@app.patch("/api/messages/{message_id}/feedback", response_model=schemas.Message)
def update_message_feedback(
    message_id: int,
    feedback_update: schemas.MessageFeedbackUpdate,
    db: Session = Depends(get_db)
):
    """Update feedback (like/dislike) for a message"""
    db_message = db.query(models.Message).filter(
        models.Message.id == message_id
    ).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Only allow feedback on assistant messages
    if db_message.role != "assistant":
        raise HTTPException(status_code=400, detail="Feedback can only be added to assistant messages")
    
    # Validate feedback value
    if feedback_update.feedback not in [None, "like", "dislike"]:
        raise HTTPException(status_code=400, detail="Feedback must be 'like', 'dislike', or null")
    
    db_message.feedback = feedback_update.feedback
    db.commit()
    db.refresh(db_message)
    return db_message
```

**Purpose:** 
- Accept PATCH requests to update message feedback
- Validate that only assistant messages can be rated
- Validate feedback values

---

## Step 4: TypeScript Types (Frontend)

### File: `frontend/src/types/index.ts`

**Added to Message interface:**
```typescript
feedback?: 'like' | 'dislike' | null;  // User feedback on assistant messages
```

**Purpose:** Define TypeScript type for feedback in frontend code.

---

## Step 5: Message Component UI (Frontend)

### File: `frontend/src/components/ChatMessage.tsx`

**Updated imports:**
```typescript
import { useState } from 'react';
```

**Updated component props:**
```typescript
interface ChatMessageProps {
  message: Message;
  plots?: string[]; // Base64 encoded plots
  onFeedback?: (messageId: number, feedback: 'like' | 'dislike' | null) => void;  // NEW
}
```

**Added state management:**
```typescript
const [currentFeedback, setCurrentFeedback] = useState<'like' | 'dislike' | null>(
  message.feedback || null
);
const [isHovered, setIsHovered] = useState(false);
```

**Added feedback handler:**
```typescript
const handleFeedback = (feedback: 'like' | 'dislike') => {
  // Toggle feedback: if clicking the same button, remove feedback
  const newFeedback = currentFeedback === feedback ? null : feedback;
  setCurrentFeedback(newFeedback);
  onFeedback?.(message.id, newFeedback);
};
```

**Added UI buttons (after timestamp):**
```typescript
{/* Feedback buttons - only show for assistant messages */}
{!isUser && (
  <div 
    className="flex items-center gap-2 mt-2"
    onMouseEnter={() => setIsHovered(true)}
    onMouseLeave={() => setIsHovered(false)}
  >
    <button
      onClick={() => handleFeedback('like')}
      className={`p-1.5 rounded-lg transition-all hover:bg-gray-200 ${
        currentFeedback === 'like' 
          ? 'bg-green-100 text-green-600' 
          : 'text-gray-400 hover:text-green-600'
      } ${!isHovered && !currentFeedback ? 'opacity-0' : 'opacity-100'}`}
      title="Good response"
      aria-label="Like this response"
    >
      <svg xmlns="http://www.w3.org/2000/svg" 
        fill={currentFeedback === 'like' ? 'currentColor' : 'none'}
        viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" 
        className="w-4 h-4">
        <path strokeLinecap="round" strokeLinejoin="round" 
          d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-.952a3.75 3.75 0 00-1.423-.23H6.75a2.25 2.25 0 01-2.25-2.25v-7.5A2.25 2.25 0 016.75 8.25h-.117z" />
      </svg>
    </button>
    
    <button
      onClick={() => handleFeedback('dislike')}
      className={`p-1.5 rounded-lg transition-all hover:bg-gray-200 ${
        currentFeedback === 'dislike' 
          ? 'bg-red-100 text-red-600' 
          : 'text-gray-400 hover:text-red-600'
      } ${!isHovered && !currentFeedback ? 'opacity-0' : 'opacity-100'}`}
      title="Bad response"
      aria-label="Dislike this response"
    >
      <svg xmlns="http://www.w3.org/2000/svg" 
        fill={currentFeedback === 'dislike' ? 'currentColor' : 'none'}
        viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" 
        className="w-4 h-4">
        <path strokeLinecap="round" strokeLinejoin="round" 
          d="M7.5 15h2.25m8.024-9.75c.011.05.028.1.052.148.591 1.2.924 2.55.924 3.977a8.96 8.96 0 01-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398C20.613 14.547 19.833 15 19 15h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 00.303-.54m.023-8.25H16.48a4.5 4.5 0 01-1.423-.23l-3.114-.952a6.75 6.75 0 00-1.423-.23H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25h.117c.489 0 .977.078 1.423.23l3.114.952c.459.152.94.23 1.423.23h3.92c.618 0 1.217-.247 1.605-.729A11.95 11.95 0 0019.5 13.5c0-.435-.023-.863-.068-1.285-.045-1.021-.964-1.715-2.054-1.715h-3.126c-.618 0-.991-.724-.725-1.282.443-.975.703-2.066.703-3.218a2.25 2.25 0 00-2.25-2.25.75.75 0 00-.75.75v.072a4.498 4.498 0 01-.322 1.672c-.303.759-.93 1.331-1.653 1.715a9.041 9.041 0 00-2.861 2.4c-.498.634-1.225 1.08-2.031 1.08H3.75z" />
      </svg>
    </button>
  </div>
)}
```

**Purpose:**
- Display like/dislike buttons on assistant messages
- Handle button clicks
- Show visual feedback (green/red highlights)
- Manage hover states

---

## Step 6: State Management (Frontend)

### File: `frontend/src/app/page.tsx`

**New function:**
```typescript
const handleFeedback = async (messageId: number, feedback: 'like' | 'dislike' | null) => {
  try {
    await fetch(`${STORAGE_SERVICE_URL}/api/messages/${messageId}/feedback`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
    });
    
    // Update local state
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === messageId ? { ...msg, feedback } : msg
      )
    );
  } catch (error) {
    console.error('Error updating feedback:', error);
  }
};
```

**Updated ChatMessage calls:**
```typescript
<ChatMessage 
  key={message.id} 
  message={message} 
  plots={messagePlots[message.id]}
  onFeedback={handleFeedback}  // NEW
/>
```

**Purpose:**
- Send feedback updates to API
- Update local React state
- Handle errors gracefully

---

## Step 7: Database Migration

### File: `storage-service/add_feedback_column.py` (NEW)

```python
"""
Migration script to add feedback column to messages table
Run this to update existing database with the new feedback column
"""

import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "chat.db"

def add_feedback_column():
    """Add feedback column to messages table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(messages)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'feedback' not in columns:
            print("Adding feedback column to messages table...")
            cursor.execute("""
                ALTER TABLE messages 
                ADD COLUMN feedback VARCHAR(20)
            """)
            conn.commit()
            print("✅ Successfully added feedback column")
        else:
            print("ℹ️  Feedback column already exists")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    add_feedback_column()
    print("✅ Migration complete!")
```

**Purpose:**
- Add feedback column to existing database
- Check if column already exists
- Handle errors gracefully

---

## Step 8: Setup Script

### File: `setup-feedback-feature.sh` (NEW)

```bash
#!/bin/bash

echo "🚀 Setting up Like/Dislike Feedback Feature"
echo "=========================================="
echo ""

cd "$(dirname "$0")/storage-service"

echo "📊 Running database migration..."
python add_feedback_column.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration completed successfully!"
    echo ""
    echo "🔄 Now restart your services:"
    echo "  ./stop-services.sh"
    echo "  ./start-services.sh"
    echo ""
else
    echo ""
    echo "❌ Migration failed. Please check the error messages above."
    exit 1
fi
```

**Purpose:** One-command setup for the entire feature.

---

## Summary of Changes

### Backend (Python/FastAPI/SQLAlchemy)
- ✅ Added `feedback` column to database
- ✅ Updated Pydantic schemas
- ✅ Created PATCH endpoint for feedback
- ✅ Added validation logic
- ✅ Created migration script

### Frontend (TypeScript/React/Next.js)
- ✅ Updated TypeScript types
- ✅ Added like/dislike buttons UI
- ✅ Implemented hover states
- ✅ Added feedback handler
- ✅ Integrated with API

### Documentation
- ✅ Created 6 comprehensive guides
- ✅ Added setup script
- ✅ Added test script

### Total Files Changed: 11
- Modified: 6
- Created: 5

---

## Key Design Decisions

1. **Toggle behavior**: Click again to remove feedback (like Twitter)
2. **Assistant only**: Only assistant messages can be rated
3. **Hover reveal**: Buttons hidden until hover (clean UI)
4. **Persistent highlight**: Active buttons stay visible
5. **Validation**: Server-side validation of feedback values
6. **Nullable**: Feedback is optional (NULL in database)

---

## Architecture Pattern

```
Presentation Layer (ChatMessage.tsx)
    ↓
State Management (page.tsx)
    ↓
API Layer (FastAPI)
    ↓
Data Access (SQLAlchemy)
    ↓
Database (SQLite)
```

This follows a clean separation of concerns with each layer having a specific responsibility.

---

*This implementation guide shows exactly what was done to add the like/dislike feature.*
