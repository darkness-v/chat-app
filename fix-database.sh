#!/bin/bash

# Quick fix script for database migration issues

echo "🔧 Database Migration Fix Script"
echo "================================="
echo ""

cd storage-service

# Check for database files
if [ -f "chat_history.db" ]; then
    echo "✓ Found chat_history.db"
    DB_FILE="chat_history.db"
elif [ -f "chat.db" ]; then
    echo "✓ Found chat.db"
    DB_FILE="chat.db"
else
    echo "❌ No database file found"
    echo "The database will be created with the correct schema when you start the service."
    exit 0
fi

echo ""
echo "Checking if image_url column exists..."

# Check if image_url column exists
if sqlite3 "$DB_FILE" "PRAGMA table_info(messages);" | grep -q "image_url"; then
    echo "✅ image_url column already exists - no migration needed"
else
    echo "⚠️  image_url column missing - running migration..."
    uv run python migrate_db.py
    
    # Verify it worked
    if sqlite3 "$DB_FILE" "PRAGMA table_info(messages);" | grep -q "image_url"; then
        echo "✅ Migration successful!"
    else
        echo "❌ Migration failed - please check the logs"
        exit 1
    fi
fi

echo ""
echo "================================="
echo "✅ Database is ready for image chat!"
echo "================================="
echo ""
echo "You can now start the services:"
echo "  cd storage-service && uv run uvicorn main:app --port 8002"
echo "  cd chat-service && uv run uvicorn main:app --port 8001"
echo ""
