from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models
import schemas
from database import engine, get_db, init_db

init_db()

app = FastAPI(title="Storage Service", version="1.0.0")

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
    
    conversation.updated_at = datetime.utcnow()
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
