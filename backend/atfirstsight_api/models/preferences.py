from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from atfirstsight_api.models.profiles import Gender


class ProfilePreferences(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    profile_id: UUID
    min_age: int | None = None
    max_age: int | None = None
    gender_pref: Gender | None = None
