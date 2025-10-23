from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
import os
import shutil
from pathlib import Path
import uuid
import json

import models
import schemas
from database import engine, get_db, init_db

init_db()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Custom JSON encoder to ensure UTC timestamps have 'Z' suffix
class CustomJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=self.custom_encoder,
        ).encode("utf-8")
    
    @staticmethod
    def custom_encoder(obj):
        if isinstance(obj, datetime):
            # Ensure timezone-aware datetime
            if obj.tzinfo is None:
                # If naive, assume UTC
                obj = obj.replace(tzinfo=timezone.utc)
            # Return ISO format with 'Z' for UTC
            return obj.isoformat().replace('+00:00', 'Z')
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

app = FastAPI(
    title="Storage Service", 
    version="1.0.0",
    default_response_class=CustomJSONResponse
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "storage"}

@app.post("/api/conversations", response_model=schemas.Conversation)
def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session = Depends(get_db)
):
    db_conversation = models.Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/api/conversations", response_model=List[schemas.Conversation])
def list_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    conversations = db.query(models.Conversation).order_by(
        models.Conversation.updated_at.desc()
    ).offset(skip).limit(limit).all()
    return conversations

@app.get("/api/conversations/{conversation_id}", response_model=schemas.ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.post("/api/conversations/{conversation_id}/messages", response_model=schemas.Message)
def add_message(
    conversation_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db_message = models.Message(
        conversation_id=conversation_id,
        **message.dict()
    )
    db.add(db_message)
    
    conversation.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    messages = db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.timestamp).all()
    return messages

@app.delete("/api/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    return {"message": "Conversation deleted"}

@app.patch("/api/conversations/{conversation_id}")
def update_conversation(
    conversation_id: int,
    conversation: schemas.ConversationUpdate,
    db: Session = Depends(get_db)
):
    db_conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.title is not None:
        db_conversation.title = conversation.title
    
    db_conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.patch("/api/messages/{message_id}/feedback", response_model=schemas.Message)
def update_message_feedback(
    message_id: int,
    feedback_update: schemas.MessageFeedbackUpdate,
    db: Session = Depends(get_db)
):
    """Update feedback (like/dislike) for a message"""
    db_message = db.query(models.Message).filter(
        models.Message.id == message_id
    ).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Only allow feedback on assistant messages
    if db_message.role != "assistant":
        raise HTTPException(status_code=400, detail="Feedback can only be added to assistant messages")
    
    # Validate feedback value
    if feedback_update.feedback not in [None, "like", "dislike"]:
        raise HTTPException(status_code=400, detail="Feedback must be 'like', 'dislike', or null")
    
    db_message.feedback = feedback_update.feedback
    db.commit()
    db.refresh(db_message)
    return db_message

@app.post("/api/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image (PNG, JPG, etc.)")
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'png'
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Return URL
    image_url = f"/uploads/{unique_filename}"
    return {"image_url": image_url}

@app.post("/api/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a CSV file for data analysis"""
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.csv"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Return file path (absolute path for code executor)
    csv_path = str(file_path.absolute())
    csv_url = f"/uploads/{unique_filename}"
    return {
        "csv_path": csv_path,
        "csv_url": csv_url,
        "filename": file.filename
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
