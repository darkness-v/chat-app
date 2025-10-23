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

# Import code executor and data analysis agent
from code_executor import CodeExecutor
from data_analysis_agent import (
    DATA_ANALYSIS_SYSTEM_PROMPT,
    extract_python_code,
    format_execution_result,
    should_retry_code,
    create_retry_prompt
)

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

# Initialize code executor for data analysis
code_executors = {}  # conversation_id -> CodeExecutor

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    image_url: Optional[str] = None  # For image-based chat
    model: Optional[str] = None

class CSVAnalysisRequest(BaseModel):
    conversation_id: int
    message: str
    csv_path: str  # Can be file path or URL
    model: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "chat"}

async def save_message(conversation_id: int, role: str, content: str, image_url: Optional[str] = None, plots: Optional[List[str]] = None):
    """Save message to storage service"""
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(
                f"{STORAGE_SERVICE_URL}/api/conversations/{conversation_id}/messages",
                json={"role": role, "content": content, "image_url": image_url, "plots": plots},
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

def get_code_executor(conversation_id: int) -> CodeExecutor:
    """Get or create a code executor for a conversation"""
    if conversation_id not in code_executors:
        code_executors[conversation_id] = CodeExecutor()
    return code_executors[conversation_id]

async def stream_csv_analysis_response(conversation_id: int, user_message: str, csv_path: str, model: str, max_retries: int = 2):
    """Stream CSV data analysis with code execution"""
    try:
        executor = get_code_executor(conversation_id)
        
        # Load CSV if not already loaded
        if not executor.list_dataframes():
            print(f"[DEBUG] Loading CSV from {csv_path}")
            success, result = executor.load_csv(csv_path, "df")
            
            if not success:
                error_msg = f"Failed to load CSV: {result}"
                yield f"data: {json.dumps({'content': error_msg, 'done': True, 'error': True})}\n\n"
                return
            
            # Send CSV info to user
            yield f"data: {json.dumps({'content': f'✅ {result}\\n\\n', 'done': False})}\n\n"
        
        # Save user message
        await save_message(conversation_id, "user", user_message)
        
        # Get conversation history
        history = await get_conversation_history(conversation_id)
        
        # Create messages with data analysis system prompt
        df_info = executor.get_dataframe_info("df") if "df" in executor.list_dataframes() else None
        messages = [
            {"role": "system", "content": DATA_ANALYSIS_SYSTEM_PROMPT}
        ]
        
        if df_info:
            messages.append({
                "role": "system", 
                "content": f"The user has loaded a dataset. Here's the information:\n\n{df_info}"
            })
        
        messages.extend(history)
        
        print(f"[DEBUG] Calling OpenAI for data analysis with model: {model}")
        
        # First LLM call - generate analysis and code
        full_response = ""
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.7,
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
        
        # Extract and execute Python code
        code_blocks = extract_python_code(full_response)
        
        print(f"[DEBUG] Extracted {len(code_blocks)} code blocks")
        
        all_plots = []  # Collect all plots for saving
        
        if code_blocks:
            yield f"data: {json.dumps({'content': '\\n\\n🔧 **Executing code...**\\n\\n', 'done': False})}\n\n"
            
            retry_count = 0
            for i, code in enumerate(code_blocks):
                print(f"[DEBUG] Executing code block {i+1}:")
                print(f"[DEBUG] Code:\n{code[:200]}...")
                
                result = executor.execute_code(code)
                print(f"[DEBUG] Execution result: success={result['success']}, plots={len(result['plots'])}")
                
                formatted_result = format_execution_result(result)
                
                # Send execution result
                yield f"data: {json.dumps({'content': formatted_result, 'done': False})}\n\n"
                
                # Send plots as base64 images and collect them
                if result['plots']:
                    all_plots.extend(result['plots'])  # Collect plots
                    for j, plot_base64 in enumerate(result['plots']):
                        plot_data = {
                            'type': 'image',
                            'data': plot_base64,
                            'done': False
                        }
                        yield f"data: {json.dumps(plot_data)}\n\n"
                
                # If code failed and should retry
                if not result['success'] and should_retry_code(result['error'], retry_count, max_retries):
                    retry_count += 1
                    print(f"[DEBUG] Retrying failed code (attempt {retry_count})")
                    
                    retry_prompt = create_retry_prompt(user_message, code, result['error'])
                    yield f"data: {json.dumps({'content': '\\n\\n🔄 **Attempting to fix the error...**\\n\\n', 'done': False})}\n\n"
                    
                    # Retry with error feedback
                    messages.append({"role": "assistant", "content": full_response})
                    messages.append({"role": "user", "content": retry_prompt})
                    
                    retry_response = ""
                    retry_stream = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=True,
                        temperature=0.7,
                    )
                    
                    async for chunk in retry_stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            retry_response += content
                            yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
                    
                    # Execute retry code
                    retry_code_blocks = extract_python_code(retry_response)
                    if retry_code_blocks:
                        for retry_code in retry_code_blocks:
                            retry_result = executor.execute_code(retry_code)
                            retry_formatted = format_execution_result(retry_result)
                            yield f"data: {json.dumps({'content': retry_formatted, 'done': False})}\n\n"
                            
                            if retry_result['plots']:
                                all_plots.extend(retry_result['plots'])  # Collect retry plots
                                for plot_base64 in retry_result['plots']:
                                    plot_data = {
                                        'type': 'image',
                                        'data': plot_base64,
                                        'done': False
                                    }
                                    yield f"data: {json.dumps(plot_data)}\n\n"
                    
                    full_response = retry_response
        
        # Save assistant response with plots
        print(f"[DEBUG] Saving assistant message with {len(all_plots)} plots")
        await save_message(conversation_id, "assistant", full_response, plots=all_plots if all_plots else None)
        
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(f"[ERROR] {error_message}")
        import traceback
        traceback.print_exc()
        yield f"data: {json.dumps({'error': error_message, 'done': True})}\n\n"

@app.post("/api/csv-analysis/stream")
async def csv_analysis_stream(request: CSVAnalysisRequest):
    """Stream CSV data analysis responses with code execution"""
    model = request.model or MODEL
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    return StreamingResponse(
        stream_csv_analysis_response(request.conversation_id, request.message, request.csv_path, model),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.post("/api/csv-analysis/clear/{conversation_id}")
async def clear_csv_analysis(conversation_id: int):
    """Clear CSV analysis data for a conversation"""
    if conversation_id in code_executors:
        code_executors[conversation_id].clear()
        del code_executors[conversation_id]
    return {"message": "CSV analysis data cleared"}

@app.get("/api/csv-analysis/dataframes/{conversation_id}")
async def list_dataframes(conversation_id: int):
    """List loaded dataframes for a conversation"""
    executor = get_code_executor(conversation_id)
    return {"dataframes": executor.list_dataframes()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
