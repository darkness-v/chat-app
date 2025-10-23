# Quick Start: Testing Conversation Management

## Prerequisites
Make sure your services are running:

```bash
cd /Users/tani/TechJDI/chat-app
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

## What's New? 🎉

### Sidebar with Conversation List
- Left sidebar shows all your conversations
- Click any conversation to load it
- Create new conversations with "+ New Chat" button
- Delete conversations with the trash icon (appears on hover)

### Auto-Generated Titles
- Your first message automatically becomes the conversation title
- Titles are truncated to 50 characters for clean display
- Titles show up immediately in the sidebar

### Mobile-Friendly
- On mobile, sidebar is hidden by default
- Click the menu button (☰) in top-left to open
- Sidebar auto-closes when you select a conversation

## Testing Steps

### Test 1: Create Multiple Conversations
1. Open http://localhost:3000
2. You should see a sidebar on the left with "+ New Chat" button
3. Send a message: "What is machine learning?"
4. Notice the conversation title updates in sidebar
5. Click "+ New Chat"
6. Send a different message: "Explain quantum computing"
7. Now you should see TWO conversations in the sidebar
8. Click between them to switch

### Test 2: Image Chat with Conversations
1. Create a new conversation
2. Upload an image using the image upload feature
3. Ask "What's in this image?"
4. Title should update to "What's in this image?"
5. Create another conversation
6. Verify the image conversation is saved in sidebar

### Test 3: CSV Analysis with Conversations
1. Create a new conversation
2. Upload a CSV file (use iris.csv or any test CSV)
3. Ask "Summarize the dataset"
4. Title becomes "Summarize the dataset"
5. Ask more questions about the data
6. Create new conversation - CSV mode should reset
7. Go back to CSV conversation
8. Continue analyzing (CSV context is maintained per conversation)

### Test 4: Delete Conversations
1. Create 3 conversations with different messages
2. Hover over a conversation in the sidebar
3. Click the trash icon that appears
4. Confirm deletion
5. Conversation should disappear from sidebar
6. Try deleting the currently active conversation
7. App should automatically create a new conversation

### Test 5: Mobile View
1. Resize your browser to mobile width (< 768px)
2. Sidebar should be hidden
3. Click the menu button (☰) in top-left corner
4. Sidebar slides in from left with dark overlay
5. Click a conversation - sidebar closes automatically
6. Click outside sidebar to close it

### Test 6: Long Titles
1. Create new conversation
2. Send a very long message: "Can you explain to me in great detail how neural networks work and what are the different types of neural networks available?"
3. Title in sidebar should be truncated: "Can you explain to me in great detail how neur..."
4. Hover over the title to see full text (if tooltip added)

## Expected Behavior

✅ Conversations persist across page refreshes  
✅ Most recent conversation loads on startup  
✅ Switching conversations loads correct message history  
✅ Deleting current conversation creates a new one  
✅ Sidebar shows relative timestamps ("2 minutes ago")  
✅ Current conversation is highlighted in sidebar  
✅ CSV mode resets when switching conversations  

## Common Issues

### Sidebar not visible
- Make sure browser width > 768px on desktop
- Check that JavaScript is enabled
- Refresh the page

### Conversations not saving
- Check that storage-service is running on port 8002
- Check browser console for API errors
- Verify database file has write permissions

### Title not updating
- Make sure you send a text message (not just image)
- Check that message has content
- Verify PATCH endpoint works: `curl -X PATCH http://localhost:8002/api/conversations/1 -H "Content-Type: application/json" -d '{"title":"Test"}'`

### Old messages showing in new conversation
- Hard refresh the page (Cmd+Shift+R / Ctrl+Shift+R)
- Check browser console for state issues
- Clear browser cache

## API Testing (Optional)

Test the backend directly:

```bash
# List all conversations
curl http://localhost:8002/api/conversations

# Create a conversation
curl -X POST http://localhost:8002/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Conversation"}'

# Update conversation title
curl -X PATCH http://localhost:8002/api/conversations/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete conversation
curl -X DELETE http://localhost:8002/api/conversations/1

# Get conversation with messages
curl http://localhost:8002/api/conversations/1
```

## Next Steps

Once everything works:
1. ✅ Read CONVERSATION_MANAGEMENT.md for full documentation
2. ✅ Customize sidebar colors in Sidebar.tsx
3. ✅ Add conversation search/filter (future enhancement)
4. ✅ Add conversation export feature (future enhancement)
5. ✅ Add conversation rename feature (future enhancement)

## Success Criteria

You've successfully tested the feature when:
- ✅ You can create multiple conversations
- ✅ You can switch between conversations and see correct messages
- ✅ Conversation titles auto-update from first message
- ✅ You can delete conversations
- ✅ Sidebar works on both desktop and mobile
- ✅ All three chat modes work (text, image, CSV)

Enjoy your new ChatGPT-like conversation management! 🚀
