from uuid import UUID
from pydantic import BaseModel

from backend.atfirstsight_api.models.chat import MessageType


class MessageCreate(BaseModel):
    content: str
    chat_id: UUID
    msg_type: MessageType
    
class MarkReadRequest(BaseModel):
    conversation_id: UUID
    last_read_message_id: UUID