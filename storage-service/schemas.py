from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime, timezone
from typing import List, Optional

class MessageBase(BaseModel):
    role: str
    content: str
    image_url: Optional[str] = None
    plots: Optional[List[str]] = None  # Base64 encoded plots
    feedback: Optional[str] = None  # 'like', 'dislike', or None

class MessageCreate(MessageBase):
    pass

class MessageFeedbackUpdate(BaseModel):
    feedback: Optional[str] = None  # 'like', 'dislike', or None

class Message(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info) -> str:
        """Ensure timestamp is UTC and has 'Z' suffix"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat().replace('+00:00', 'Z')

class ConversationBase(BaseModel):
    title: Optional[str] = "New Conversation"

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime, _info) -> str:
        """Ensure datetime is UTC and has 'Z' suffix"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat().replace('+00:00', 'Z')

class ConversationWithMessages(Conversation):
    messages: List[Message] = []
    
    model_config = ConfigDict(from_attributes=True)
