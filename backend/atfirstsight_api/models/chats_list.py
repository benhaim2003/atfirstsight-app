from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from .chats import ChatParticipant, MessageType

class LastMessage(BaseModel):
    sender_id: UUID
    type: MessageType
    created_at: datetime
    content: str
    

    model_config = { "from_attributes": True }


class ChatPreview(BaseModel):
    chat_id: UUID
    other_participant: ChatParticipant 
    last_message: Optional[LastMessage] = None
    unread_count: int = 0

    model_config = { "from_attributes": True }


class ChatListResponse(BaseModel):
    chats: list[ChatPreview]