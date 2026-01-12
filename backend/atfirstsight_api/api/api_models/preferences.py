from pydantic import BaseModel

from atfirstsight_api.models.profiles import Gender


class ProfilePreferencesCreate(BaseModel):
    min_age: int | None = None
    max_age: int | None = None
    gender_pref: Gender | None = None
