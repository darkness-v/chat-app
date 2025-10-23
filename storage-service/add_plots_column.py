"""
Add plots column to messages table
Run this script to migrate existing database
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "chat_history.db")

def add_plots_column():
    """Add plots column to messages table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(messages)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'plots' not in columns:
            print("Adding 'plots' column to messages table...")
            cursor.execute("ALTER TABLE messages ADD COLUMN plots TEXT")
            conn.commit()
            print("✅ Column added successfully!")
        else:
            print("Column 'plots' already exists. No migration needed.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_plots_column()
