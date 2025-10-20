# Troubleshooting Guide

## Issue Fixed: Model Name Error

### Problem
The assistant was not returning responses because the model name was set to `gpt-5-mini` which doesn't exist.

### Solution
Updated `chat-service/.env` to use `gpt-4o-mini`:

```bash
MODEL=gpt-4o-mini
```

## Current Services Status

✅ **Storage Service** - Running on port 8002 (with auto-reload)
✅ **Chat Service** - Running on port 8001 (with auto-reload)  
✅ **Frontend** - Running on port 3000

### Services are now running with debug logging enabled!

## How to Test

1. **Open the app**: http://localhost:3000

2. **Send a test message**: Type "Hello, how are you?" and press Send

3. **Check logs**: Watch the chat service terminal for debug output:
   ```
   [DEBUG] Saving user message for conversation X
   [DEBUG] Getting conversation history
   [DEBUG] History has Y messages
   [DEBUG] Calling OpenAI with model: gpt-4o-mini
   [DEBUG] Starting to stream response
   [DEBUG] Finished streaming. Saving assistant message
   ```

## Common Issues & Solutions

### 1. No response from assistant
**Symptoms**: Message sent but no response appears
**Causes**:
- ❌ Invalid OpenAI API key
- ❌ Wrong model name (e.g., gpt-5-mini instead of gpt-4o-mini)
- ❌ Network issues

**Solutions**:
```bash
# Check your API key in chat-service/.env
cat chat-service/.env

# Valid models:
# - gpt-4o-mini (recommended, fast & cheap)
# - gpt-4o
# - gpt-3.5-turbo
# - gpt-4-turbo
```

### 2. Port already in use
**Symptoms**: `Address already in use` error
**Solution**:
```bash
# Kill process on specific port
lsof -ti:8001 | xargs kill -9  # Chat service
lsof -ti:8002 | xargs kill -9  # Storage service
lsof -ti:3000 | xargs kill -9  # Frontend

# Then restart the services
```

### 3. CORS errors in browser
**Symptoms**: Console shows CORS policy errors
**Solution**: Already configured! Both backend services have CORS enabled:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Database errors
**Symptoms**: "Conversation not found" or database errors
**Solution**:
```bash
# Reset database
cd storage-service
rm conversations.db
# Service will auto-create new database
```

### 5. Frontend not updating
**Symptoms**: Old UI or changes not reflected
**Solution**:
```bash
# Clear Next.js cache
cd frontend
rm -rf .next
npm run dev
```

## Checking Service Health

### Storage Service
```bash
curl http://localhost:8002/health
# Expected: {"status":"healthy","service":"storage"}
```

### Chat Service
```bash
curl http://localhost:8001/health
# Expected: {"status":"healthy","service":"chat"}
```

### Test Full Flow
```bash
# 1. Create conversation
curl -X POST http://localhost:8002/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}'

# 2. Send message (non-streaming)
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":1,"message":"Say hello!"}'
```

## Debug Mode

The chat service now has extensive debug logging. Watch the terminal for:

```
[DEBUG] Saving user message for conversation 1
[DEBUG] Getting conversation history
[DEBUG] History has 0 messages
[DEBUG] Calling OpenAI with model: gpt-4o-mini
[DEBUG] Starting to stream response
[DEBUG] Finished streaming. Saving assistant message
```

If you see an `[ERROR]` message, that's where the problem is!

## Performance Tips

1. **Use gpt-4o-mini** for faster responses and lower cost
2. **Enable streaming** for real-time user experience (already enabled!)
3. **Database location**: `storage-service/conversations.db` - backup regularly

## OpenAI API Key Issues

### Invalid key errors:
```
Error: Incorrect API key provided
```

**Solution**: Verify your key at https://platform.openai.com/api-keys

### Rate limit errors:
```
Error: Rate limit exceeded
```

**Solution**: Wait a moment or upgrade your OpenAI plan

### No credits:
```
Error: You exceeded your current quota
```

**Solution**: Add credits to your OpenAI account

## Restart Everything Fresh

```bash
# Terminal 1 - Storage Service
cd chat-app/storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 2 - Chat Service  
cd chat-app/chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 3 - Frontend
cd chat-app/frontend
npm run dev
```

## Success Indicators

✅ All services show "Application startup complete"
✅ Browser console shows no errors
✅ Messages appear with timestamps
✅ Assistant responses stream in real-time
✅ Chat history persists across page refreshes

## Need More Help?

Check the service logs in each terminal window for detailed error messages!
