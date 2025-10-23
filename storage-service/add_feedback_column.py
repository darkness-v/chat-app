"""
Migration script to add feedback column to messages table
Run this to update existing database with the new feedback column
"""

import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "chat_history.db"

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
