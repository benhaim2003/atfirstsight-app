import uuid
from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError

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


class ChatParticipant(BaseModel):
    profile_id: UUID
    username: str
    primary_photo_url: str | None
    

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    chat_id: UUID
    sender_id: UUID
    msg_type: MessageType = MessageType.TEXT
    content: str
    metadata: ImageMetaData | AudioMetaData | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: datetime | None = None
    
    @model_validator(mode='after')
    def validate_metadata_matches_type(self):        

        if self.msg_type == MessageType.TEXT:
            if self.metadata is not None:
                raise ValueError("Text messages should not have metadata.")

        elif self.msg_type == MessageType.IMAGE:
            if not isinstance(self.metadata, ImageMetaData):
                raise ValueError("Image messages must have ImageMetaData.")

        elif self.msg_type == MessageType.AUDIO:
            if not isinstance(self.metadata, AudioMetaData):
                raise ValueError("Audio messages must have AudioMetaData.")
            
        return self


class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    participant_a: ChatParticipant
    participant_b: ChatParticipant
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    messages: list[Message]
