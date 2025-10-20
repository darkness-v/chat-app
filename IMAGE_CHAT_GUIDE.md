# Image Chat Feature - Setup Guide

## Overview
Added image chatting capability to the multi-turn chat application. Users can now:
- Upload images (PNG/JPG/JPEG)
- Preview images be### Vision API errors
- Ensure using `gpt-4o` or `gpt-4o-mini` model
- Verify OpenAI API key has vision access
- Images are automatically converted to base64 (no public URL needed)

### OpenAI error "invalid_image_url"
This was fixed! Images are now sent as base64 data instead of localhost URLs.
If you see this error, restart the chat service to apply the fix.

### Images not displayingending
- Chat with AI about images using GPT-4 Vision
- View images in conversation history

## Changes Made

### Backend (Storage Service)
1. **Database Schema**: Added `image_url` column to messages table
2. **Image Upload Endpoint**: `/api/upload-image` - handles file uploads
3. **Static File Serving**: Mounted `/uploads` directory for serving images
4. **Dependencies**: Added `python-multipart` and `aiofiles` for file handling

### Backend (Chat Service)
1. **Vision Model Support**: Automatically uses GPT-4 Vision when images are present
2. **Message Format**: Updated to support OpenAI's vision API format
3. **History Context**: Images are included in conversation history

### Frontend
1. **ChatInput Component**: Added image upload button and preview
2. **ChatMessage Component**: Displays images in messages
3. **Main Page**: Handles image upload before sending messages
4. **Types**: Added optional `image_url` field to Message interface

## Setup Instructions

### 1. Update Backend Dependencies

```bash
# Storage Service
cd chat-app/storage-service
pip install -r requirements.txt

# Chat Service (no changes needed, but verify)
cd ../chat-service
pip install -r requirements.txt
```

### 2. Database Migration

If you have an existing database, run the migration:

```bash
cd chat-app/storage-service
python migrate_db.py
```

If starting fresh, the database will be created with the new schema automatically.

### 3. Environment Variables

Make sure your chat service has the OpenAI API key set:

```bash
# In chat-service/.env
OPENAI_API_KEY=your_api_key_here
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o  # or gpt-4o-mini for vision
```

### 4. Create Uploads Directory

```bash
cd chat-app/storage-service
mkdir -p uploads
```

### 5. Start Services

```bash
# Terminal 1 - Storage Service
cd chat-app/storage-service
python main.py

# Terminal 2 - Chat Service
cd chat-app/chat-service
python main.py

# Terminal 3 - Frontend
cd chat-app/frontend
npm run dev
```

## Usage

1. Open http://localhost:3000
2. Click the image icon (📷) to upload an image
3. Preview appears - you can remove it with the × button
4. Type a message or leave blank (will ask "What is in this image?")
5. Click Send
6. AI will analyze the image and respond
7. Images appear in conversation history

## Technical Details

### Image Flow
1. User selects image → Preview shown in ChatInput
2. On send → Image uploaded to Storage Service → Returns URL
3. Message created with `image_url` field
4. Chat Service receives request with image URL
5. **Chat Service fetches image and converts to base64**
6. Chat Service formats message for OpenAI Vision API (with base64 data)
7. Response streamed back to frontend
8. Both user message and AI response saved to database

**Why base64?** OpenAI's API cannot access localhost URLs. We convert images to base64 data URLs so they can be sent directly in the API request.

### Model Selection
- Text-only messages: Uses configured model (default: gpt-4o-mini)
- Messages with images: Automatically uses gpt-4o (Vision capable)

### Storage
- Images stored in `storage-service/uploads/`
- Filenames: UUID-based to prevent conflicts
- URLs stored in database as `/uploads/{filename}`
- Served via FastAPI StaticFiles

## API Updates

### Storage Service

**New Endpoint:**
```
POST /api/upload-image
Content-Type: multipart/form-data

Response: { "image_url": "/uploads/{uuid}.{ext}" }
```

**Updated Endpoint:**
```
POST /api/conversations/{id}/messages
Body: {
  "role": "user",
  "content": "Message text",
  "image_url": "/uploads/..." // Optional
}
```

### Chat Service

**Updated Endpoint:**
```
POST /api/chat/stream
Body: {
  "conversation_id": 1,
  "message": "What's in this image?",
  "image_url": "/uploads/..." // Optional
}
```

## Troubleshooting

### Images not uploading
- Check `uploads/` directory exists
- Verify python-multipart is installed
- Check file permissions on uploads directory

### Database Error: "no such column: messages.image_url"

This means your database was created before the image feature was added.

**Quick Fix:**
```bash
./fix-database.sh
```

**Manual Fix:**
```bash
cd storage-service
uv run python migrate_db.py
```

**Alternative (Nuclear Option):**
```bash
cd storage-service
rm chat_history.db  # WARNING: Deletes all conversations!
# Restart storage service to create new DB with correct schema
```

### Vision API errors
- Ensure using gpt-4o or gpt-4-vision-preview model
- Verify OpenAI API key has vision access
- Check image URL is accessible from chat service

### Images not displaying
- Verify STORAGE_SERVICE_URL is correct in frontend
- Check CORS settings allow image access
- Confirm StaticFiles is mounted in storage service

## Cost Considerations

GPT-4 Vision is more expensive than text-only models:
- Text: ~$0.01 per 1K tokens
- Vision: ~$0.01 per image + text tokens

Consider setting usage limits or using gpt-4o-mini for lower costs.
