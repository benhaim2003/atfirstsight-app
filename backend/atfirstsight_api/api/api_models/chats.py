from typing import Union, Literal
from uuid import UUID

from pydantic import BaseModel

from backend.atfirstsight_api.models.chats import MessageType, AudioMetaData, ImageMetaData


class MarkReadRequest(BaseModel):
    chat_id: UUID


class CreateTextMessageRequest(BaseModel):
    msg_type: Literal[MessageType.TEXT] = MessageType.TEXT
    content: str
    metadata: None = None


class CreateImageMessageRequest(BaseModel):
    msg_type: Literal[MessageType.IMAGE] = MessageType.IMAGE
    content: str
    metadata: ImageMetaData


class CreateAudioMessageRequest(BaseModel):
    msg_type: Literal[MessageType.AUDIO] = MessageType.AUDIO
    content: str
    metadata: AudioMetaData


CreateMessageSchema = Union[CreateTextMessageRequest, CreateImageMessageRequest, CreateAudioMessageRequest]
