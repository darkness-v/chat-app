from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import httpx
from openai import AsyncOpenAI
import json
import base64

load_dotenv()

app = FastAPI(title="Chat Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://localhost:8002")
MODEL = os.getenv("MODEL", "gpt-5-mini")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    image_url: Optional[str] = None  # For image-based chat
    model: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "chat"}

async def save_message(conversation_id: int, role: str, content: str, image_url: Optional[str] = None):
    """Save message to storage service"""
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(
                f"{STORAGE_SERVICE_URL}/api/conversations/{conversation_id}/messages",
                json={"role": role, "content": content, "image_url": image_url},
                timeout=10.0
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Error saving message: {e}")

async def get_image_as_base64(image_url: str) -> str:
    """Download image from storage service and convert to base64 data URL"""
    async with httpx.AsyncClient() as http_client:
        try:
            full_url = f"{STORAGE_SERVICE_URL}{image_url}"
            response = await http_client.get(full_url, timeout=10.0)
            response.raise_for_status()
            
            # Get image content type
            content_type = response.headers.get('content-type', 'image/png')
            
            # Convert to base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            data_url = f"data:{content_type};base64,{image_data}"
            
            return data_url
        except Exception as e:
            print(f"Error fetching image: {e}")
            raise

async def get_conversation_history(conversation_id: int) -> List[dict]:
    """Get conversation history from storage service"""
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.get(
                f"{STORAGE_SERVICE_URL}/api/conversations/{conversation_id}/messages",
                timeout=10.0
            )
            response.raise_for_status()
            messages = response.json()
        
            formatted_messages = []
            for msg in messages:
                if msg.get("image_url"):
                    # Convert image to base64 data URL
                    try:
                        image_data_url = await get_image_as_base64(msg["image_url"])
                        formatted_messages.append({
                            "role": msg["role"],
                            "content": [
                                {"type": "text", "text": msg["content"]},
                                {"type": "image_url", "image_url": {"url": image_data_url}}
                            ]
                        })
                    except Exception as e:
                        print(f"Error converting image to base64: {e}")
                        # Fallback: just send text without image
                        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
                else:
                    # Regular text message
                    formatted_messages.append({"role": msg["role"], "content": msg["content"]})
            return formatted_messages
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

async def stream_chat_response(conversation_id: int, user_message: str, model: str, image_url: Optional[str] = None):
    """Stream chat response from OpenAI"""
    try:
        print(f"[DEBUG] Saving user message for conversation {conversation_id}")
        await save_message(conversation_id, "user", user_message, image_url)
       
        print(f"[DEBUG] Getting conversation history")
        history = await get_conversation_history(conversation_id)
        print(f"[DEBUG] History has {len(history)} messages")
    
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ] + history
        
        print(f"[DEBUG] Calling OpenAI with model: {model}")
        full_response = ""
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.7,
        )
        
        print(f"[DEBUG] Starting to stream response")
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
        
        print(f"[DEBUG] Finished streaming. Saving assistant message")
        await save_message(conversation_id, "assistant", full_response)
        
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(f"[ERROR] {error_message}")
        import traceback
        traceback.print_exc()
        yield f"data: {json.dumps({'error': error_message, 'done': True})}\n\n"

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses"""
    if request.image_url:
        model = request.model or "gpt-4o"  
    else:
        model = request.model or MODEL
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    return StreamingResponse(
        stream_chat_response(request.conversation_id, request.message, model, request.image_url),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint (for testing)"""
    try:
        await save_message(request.conversation_id, "user", request.message, request.image_url)
        
        history = await get_conversation_history(request.conversation_id)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ] + history
        
        if request.image_url:
            model = request.model or "gpt-4o"
        else:
            model = request.model or MODEL
            
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        
        assistant_message = response.choices[0].message.content
        
        await save_message(request.conversation_id, "assistant", assistant_message)
        
        return {"response": assistant_message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
