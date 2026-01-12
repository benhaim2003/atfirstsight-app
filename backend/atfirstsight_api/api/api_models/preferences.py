from pydantic import BaseModel

from atfirstsight_api.models.profiles import Gender


class ProfilePreferencesCreate(BaseModel):
    min_age: int | None = None
    max_age: int | None = None
    gender_pref: list[Gender] | None = None
