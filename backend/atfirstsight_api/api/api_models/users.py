from uuid import UUID

from pydantic import BaseModel


class UserCredentials(BaseModel):
    email: str
    password: str


class UserSigninResponse(BaseModel):
    id: UUID
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: int
    token_type: str
