import uuid
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Literal, Union
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class ImageMetaData(BaseModel):
    width: int
    height: int
    aspect_ratio: str


class AudioMetaData(BaseModel):
    duration_seconds: float
    waveform: list[float]


class MessageBase(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    chat_id: UUID
    sender_id: UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: datetime | None = None


class TextMessage(MessageBase):
    msg_type: Literal[MessageType.TEXT] = MessageType.TEXT
    metadata: None = None


class ImageMessage(MessageBase):
    msg_type: Literal[MessageType.IMAGE] = MessageType.IMAGE
    metadata: ImageMetaData


class AudioMessage(MessageBase):
    msg_type: Literal[MessageType.AUDIO] = MessageType.AUDIO
    metadata: AudioMetaData


Message = Union[TextMessage, ImageMessage, AudioMessage]


class ChatParticipant(BaseModel):
    profile_id: UUID
    username: str
    primary_photo_url: str | None = None


class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    participant_a: ChatParticipant
    participant_b: ChatParticipant
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ChatsListItem(BaseModel):
    chat: Chat
    last_message: Message | None = None


class ChatsList(BaseModel):
    chats: list[ChatsListItem] | None = None
