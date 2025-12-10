from datetime import date

from pydantic import BaseModel

from atfirstsight_api.models.profiles import Gender


class ProfileCreate(BaseModel):
    username: str
    bio: str
    gender: Gender
    birth_date: date
