import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str
    
class Message(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    chat_id: UUID
    sender_id: UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: datetime | None = None
    
    class Config:
        from_attributes = True


class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    profile_a_id: UUID
    profile_b_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True



class ChatParticipant(BaseModel):
    profile_id: UUID
    username: str
    # primary_photo_url: str | None
    class Config:
        from_attributes = True


class ChatSession(BaseModel):
    chat_id: UUID
    other_participant: ChatParticipant
    messages: list[Message]