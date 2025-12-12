from uuid import UUID
from pydantic import BaseModel

from backend.atfirstsight_api.models.chats import MessageType


class MessageCreate(BaseModel):
    chat_id: UUID
    type: MessageType
    content: str
    
class MarkReadRequest(BaseModel):
    chat_id: UUID
    last_read_message_id: UUID