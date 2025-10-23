# CSV Plot Display Bug - Fixed! ✅

## Problem Summary

When uploading a CSV file and asking the AI to generate plots (e.g., histograms), the code was being generated and executed successfully, but **the diagrams were not appearing in the chat interface**.

## Root Cause Analysis

The bug was caused by a **state management issue** in the frontend:

1. **During Streaming**: 
   - Plots were captured correctly from the backend as base64 images
   - Stored in the `messagePlots` state with temporary message IDs
   - Displayed correctly during the streaming phase

2. **After Streaming**:
   - The code called `loadMessages()` to reload all messages from the database
   - This replaced the entire `messages` state with fresh data from the DB
   - The new messages had **different IDs** from the database
   - The `messagePlots` mapping still referenced the **old streaming message IDs**
   - Result: Plots were lost because the ID mapping was broken

## Solution Implemented

We implemented a **proper persistent storage solution** for plots:

### Backend Changes

1. **Database Schema** (`storage-service/models.py`):
   - Added `plots` column to the `Message` table to store base64 encoded plots
   ```python
   plots = Column(JSON, nullable=True)  # Store base64 encoded plots
   ```

2. **API Schema** (`storage-service/schemas.py`):
   - Updated `MessageBase` to include plots field
   ```python
   plots: Optional[List[str]] = None  # Base64 encoded plots
   ```

3. **Chat Service** (`chat-service/main.py`):
   - Modified `save_message()` function to accept plots parameter
   - Collected all plots from code execution in the streaming function
   - Saved plots along with the assistant message to the database
   ```python
   all_plots = []  # Collect all plots
   # ... execute code and collect plots ...
   await save_message(conversation_id, "assistant", full_response, plots=all_plots)
   ```

4. **Database Migration** (`storage-service/add_plots_column.py`):
   - Created a migration script to add the `plots` column to existing databases
   - Safely checks if column exists before adding it

### Frontend Changes

1. **TypeScript Types** (`frontend/src/types/index.ts`):
   - Added `plots` field to the `Message` interface
   ```typescript
   plots?: string[];  // Base64 encoded plots
   ```

2. **Message Loading** (`frontend/src/app/page.tsx`):
   - Updated `loadMessages()` to populate `messagePlots` state from database
   ```typescript
   const plots: Record<number, string[]> = {};
   data.forEach((msg: Message) => {
     if (msg.plots && msg.plots.length > 0) {
       plots[msg.id] = msg.plots;
     }
   });
   setMessagePlots(plots);
   ```

3. **Display Component** (`frontend/src/components/ChatMessage.tsx`):
   - Already had proper plot rendering logic (no changes needed)
   - Displays plots from the `plots` prop

## How It Works Now

### CSV Upload and Analysis Flow:

1. **User uploads CSV** → File saved to storage service
2. **User asks for plot** → AI generates Python code with matplotlib
3. **Code execution** → Backend executes code and captures plots as base64
4. **Streaming response**:
   - AI response text streamed to frontend
   - Plots sent as `{type: 'image', data: base64_string}` events
   - Frontend displays plots in real-time
5. **Saving to database**:
   - All plots collected during execution
   - Saved with the assistant message in the database
6. **After streaming**:
   - Messages reloaded from database
   - Plots loaded from database and mapped to correct message IDs
   - **Plots persist correctly** ✅

### Benefits of This Solution:

✅ **Persistence**: Plots are saved in the database and survive page refreshes  
✅ **Consistency**: Message IDs from database match plot mappings  
✅ **Reliability**: No more ID mismatch issues  
✅ **Scalability**: Can store multiple plots per message  
✅ **Clean Architecture**: Backend is the source of truth for all message data  

## Files Modified

### Backend:
- `chat-app/storage-service/models.py` - Added plots column
- `chat-app/storage-service/schemas.py` - Added plots field to schema
- `chat-app/chat-service/main.py` - Updated save_message and streaming logic
- `chat-app/storage-service/add_plots_column.py` - Migration script (new file)

### Frontend:
- `chat-app/frontend/src/types/index.ts` - Added plots to Message type
- `chat-app/frontend/src/app/page.tsx` - Updated loadMessages to load plots

## Testing the Fix

1. **Upload a CSV file** (e.g., iris.csv)
2. **Ask for a plot**: "Create a histogram of sepal_length"
3. **Verify**:
   - ✅ Code is generated and shown in a code block
   - ✅ Plot appears below the code
   - ✅ Refresh the page - plot still appears
   - ✅ Multiple plots work correctly
   - ✅ Plot persists across sessions

## Migration Instructions

If you have an existing database, run the migration:

```bash
cd chat-app/storage-service
python add_plots_column.py
```

Then restart the services:

```bash
cd chat-app
./stop-services.sh
./start-services.sh
```

## Technical Notes

- **Plot Format**: Base64 encoded PNG images
- **Storage**: SQLite JSON column (text-based storage for SQLAlchemy)
- **Size Considerations**: Base64 encoding increases size by ~33%
- **Alternative**: For production, consider storing plots as files and saving URLs instead

## Future Improvements

1. **File-based storage**: Store plots as separate image files for better performance
2. **Plot compression**: Compress plots before storing
3. **Plot caching**: Cache frequently accessed plots
4. **Plot metadata**: Store plot dimensions, type, etc.
5. **Plot deletion**: Clean up old plots to manage database size

---

**Status**: ✅ Fixed and Deployed  
**Date**: October 23, 2025  
**Services Running**: 
- Storage Service: http://localhost:8002
- Chat Service: http://localhost:8001
- Frontend: http://localhost:3000
