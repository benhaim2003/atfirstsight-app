import uuid
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class ApproachRequestStatus(StrEnum):
    Pending = "pending"
    Accepted = "accepted"
    Denied = "denied"
    Expired = "expired"
    # TODO
    Verified = "verified"


class ApproachRequest(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    requester_id: UUID
    receiver_id: UUID
    status: ApproachRequestStatus
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
