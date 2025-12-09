import uuid
from datetime import datetime, date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class Gender(StrEnum):
    Male = "male"
    Female = "female"
    Other = "other"


class ProfileStatus(StrEnum):
    Offline = "offline"
    Online = "online"


class ProfilePhoto(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    storage_path: str
    sort_order: int
    uploaded_at: datetime = Field(default_factory=datetime.now)


class Profile(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    username: str
    bio: str
    gender: Gender
    birth_date: date
    status: ProfileStatus
    photos: list[ProfilePhoto]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
