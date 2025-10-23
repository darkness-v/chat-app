#!/bin/bash

# Test script for like/dislike feedback feature
# This script tests the API endpoints and verifies functionality

echo "🧪 Testing Like/Dislike Feedback Feature"
echo "========================================"
echo ""

STORAGE_URL="http://localhost:8002"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if storage service is running
echo "1. Checking if storage service is running..."
if curl -s "${STORAGE_URL}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Storage service is running${NC}"
else
    echo -e "${RED}❌ Storage service is not running${NC}"
    echo "   Start it with: cd storage-service && uv run uvicorn main:app --host 0.0.0.0 --port 8002"
    exit 1
fi
echo ""

# Create a test conversation
echo "2. Creating test conversation..."
CONV_RESPONSE=$(curl -s -X POST "${STORAGE_URL}/api/conversations" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Feedback Feature"}')
CONV_ID=$(echo $CONV_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo -e "${GREEN}✅ Created conversation ID: ${CONV_ID}${NC}"
echo ""

# Add a user message
echo "3. Adding user message..."
USER_MSG=$(curl -s -X POST "${STORAGE_URL}/api/conversations/${CONV_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"role":"user","content":"What is machine learning?"}')
echo -e "${GREEN}✅ User message added${NC}"
echo ""

# Add an assistant message
echo "4. Adding assistant message..."
ASSISTANT_MSG=$(curl -s -X POST "${STORAGE_URL}/api/conversations/${CONV_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"role":"assistant","content":"Machine learning is a subset of AI that enables computers to learn from data without being explicitly programmed."}')
MSG_ID=$(echo $ASSISTANT_MSG | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo -e "${GREEN}✅ Assistant message added (ID: ${MSG_ID})${NC}"
echo ""

# Test liking the message
echo "5. Testing LIKE feedback..."
LIKE_RESPONSE=$(curl -s -X PATCH "${STORAGE_URL}/api/messages/${MSG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"feedback":"like"}')
if echo $LIKE_RESPONSE | grep -q '"feedback":"like"'; then
    echo -e "${GREEN}✅ Like feedback successful${NC}"
else
    echo -e "${RED}❌ Like feedback failed${NC}"
    echo "Response: $LIKE_RESPONSE"
fi
echo ""

# Test disliking the message
echo "6. Testing DISLIKE feedback..."
DISLIKE_RESPONSE=$(curl -s -X PATCH "${STORAGE_URL}/api/messages/${MSG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"feedback":"dislike"}')
if echo $DISLIKE_RESPONSE | grep -q '"feedback":"dislike"'; then
    echo -e "${GREEN}✅ Dislike feedback successful${NC}"
else
    echo -e "${RED}❌ Dislike feedback failed${NC}"
    echo "Response: $DISLIKE_RESPONSE"
fi
echo ""

# Test removing feedback
echo "7. Testing REMOVE feedback..."
REMOVE_RESPONSE=$(curl -s -X PATCH "${STORAGE_URL}/api/messages/${MSG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"feedback":null}')
if echo $REMOVE_RESPONSE | grep -q '"feedback":null' || ! echo $REMOVE_RESPONSE | grep -q '"feedback"'; then
    echo -e "${GREEN}✅ Remove feedback successful${NC}"
else
    echo -e "${RED}❌ Remove feedback failed${NC}"
    echo "Response: $REMOVE_RESPONSE"
fi
echo ""

# Test invalid feedback value
echo "8. Testing INVALID feedback (should fail)..."
INVALID_RESPONSE=$(curl -s -X PATCH "${STORAGE_URL}/api/messages/${MSG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"feedback":"invalid"}')
if echo $INVALID_RESPONSE | grep -q '"detail"'; then
    echo -e "${GREEN}✅ Correctly rejected invalid feedback${NC}"
else
    echo -e "${YELLOW}⚠️  Invalid feedback was accepted (should be rejected)${NC}"
fi
echo ""

# Verify feedback persists
echo "9. Verifying feedback persistence..."
curl -s -X PATCH "${STORAGE_URL}/api/messages/${MSG_ID}/feedback" \
  -H "Content-Type: application/json" \
  -d '{"feedback":"like"}' > /dev/null
  
GET_RESPONSE=$(curl -s "${STORAGE_URL}/api/conversations/${CONV_ID}")
if echo $GET_RESPONSE | grep -q '"feedback":"like"'; then
    echo -e "${GREEN}✅ Feedback persists correctly${NC}"
else
    echo -e "${RED}❌ Feedback not persisting${NC}"
fi
echo ""

# Check database directly
echo "10. Checking database schema..."
cd "$(dirname "$0")/storage-service"
if [ -f "chat.db" ]; then
    SCHEMA=$(sqlite3 chat.db "PRAGMA table_info(messages);" | grep feedback)
    if [ -n "$SCHEMA" ]; then
        echo -e "${GREEN}✅ Feedback column exists in database${NC}"
        echo "   Schema: $SCHEMA"
    else
        echo -e "${RED}❌ Feedback column NOT found in database${NC}"
        echo "   Run: python add_feedback_column.py"
    fi
else
    echo -e "${YELLOW}⚠️  Database file not found${NC}"
fi
echo ""

# Summary
echo "========================================"
echo -e "${GREEN}🎉 Testing Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000"
echo "2. Send a message to the assistant"
echo "3. Hover over the response"
echo "4. Click 👍 or 👎"
echo "5. Refresh the page - feedback should persist!"
echo ""
echo "📖 Read FEEDBACK_FEATURE.md for full documentation"
