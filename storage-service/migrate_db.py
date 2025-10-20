"""
Database migration script to add image_url column to messages table
"""
import sqlite3
import os

DB_PATH = "chat_history.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(messages)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'image_url' not in columns:
            print("Adding image_url column to messages table...")
            cursor.execute("ALTER TABLE messages ADD COLUMN image_url VARCHAR(500)")
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("image_url column already exists. No migration needed.")
    
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        migrate()
    else:
        print(f"Database {DB_PATH} not found. It will be created with the new schema on first run.")
