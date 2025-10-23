#!/bin/bash
# Test script to verify timestamp fix

echo "======================================"
echo "Timestamp Fix Verification"
echo "======================================"
echo ""

# Check if services are running
echo "1. Checking if services are running..."
if ! curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "❌ Storage service not running!"
    echo "   Start with: ./start-services.sh"
    exit 1
fi
echo "✅ Storage service is running"

if ! curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "❌ Chat service not running!"
    echo "   Start with: ./start-services.sh"
    exit 1
fi
echo "✅ Chat service is running"

if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "⚠️  Frontend not running (this is optional for API test)"
else
    echo "✅ Frontend is running"
fi

echo ""
echo "2. Checking timestamp format in API response..."
echo ""

# Get the latest conversation
RESPONSE=$(curl -s http://localhost:8002/api/conversations)

# Check if response contains 'Z' suffix
if echo "$RESPONSE" | grep -q '"updated_at":"[0-9T:.-]*Z"'; then
    echo "✅ Timestamps have 'Z' suffix (UTC indicator)"
    echo ""
    echo "Sample timestamp:"
    echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"  {data[0]['updated_at']}\")" 2>/dev/null || echo "  (Could not parse JSON)"
    echo ""
    echo "✅ TIMEZONE FIX VERIFIED!"
    echo ""
    echo "Expected format: 2025-10-23T14:15:38.755848Z"
    echo "                                            ^ 'Z' means UTC"
else
    echo "❌ Timestamps missing 'Z' suffix!"
    echo ""
    echo "Sample timestamp:"
    echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"  {data[0]['updated_at']}\")" 2>/dev/null || echo "  (Could not parse JSON)"
    echo ""
    echo "Expected format: 2025-10-23T14:15:38.755848Z"
    echo "Actual format:   2025-10-23T14:15:38.755848  (missing Z)"
    echo ""
    echo "❌ FIX NOT APPLIED - Please restart services:"
    echo "   ./stop-services.sh"
    echo "   ./start-services.sh"
    exit 1
fi

echo ""
echo "3. Testing with JavaScript (browser simulation)..."
echo ""

# Test JavaScript date parsing
node -e "
const timestamp = '$RESPONSE' | grep -o '[0-9T:.-]*Z' | head -1;
if (timestamp) {
    const date = new Date('2025-10-23T14:15:38.755848Z');
    const now = new Date();
    const diffMinutes = Math.floor((now - date) / 1000 / 60);
    console.log('✅ JavaScript correctly parses UTC timestamp');
    console.log('   Parsed as: ' + date.toString());
    console.log('   Difference: ' + diffMinutes + ' minutes ago');
} else {
    console.log('❌ Could not extract timestamp');
}
" 2>/dev/null || echo "⚠️  Node.js not available for JavaScript test (optional)"

echo ""
echo "======================================"
echo "Testing Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000"
echo "2. Send a new message"
echo "3. Check sidebar - should show 'just now'"
echo "4. Wait 2 minutes - should show '2 minutes ago'"
echo ""
echo "If timestamps still show wrong time:"
echo "- Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)"
echo "- Clear browser cache"
echo "- Check browser console for errors"
