from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from .chat import ChatParticipant

class LastMessage(BaseModel):
    """A model for the last message preview in a chat list."""
    content: str
    created_at: datetime
    sender_id: UUID

    model_config = { "from_attributes": True }


class ChatPreview(BaseModel):
    """
    The main model for a single item in the chat list.
    Contains the chat ID, the *other* person, and the last message.
    """
    chat_id: UUID
    other_participant: ChatParticipant  # We reuse the model from get_chat_session
    last_message: Optional[LastMessage] = None
    unread_count: int = 0  # We can implement this logic later

    model_config = { "from_attributes": True }


class ChatListResponse(BaseModel):
    """The final response object the API will send."""
    chats: list[ChatPreview]