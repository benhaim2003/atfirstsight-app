from fastapi import HTTPException, APIRouter
from pydantic import field_validator, BaseModel

from atfirstsight_api.api.dependencies.auth import UserDep
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.db.exceptions import DBException
from atfirstsight_api.models.chats import ChatsList
from uuid import UUID


router = APIRouter()


@router.get("/chats", response_model=ChatsList, tags=["Chat"],
            summary="Retrieve a list of the user's chats")
async def get_user_chat_list(
        db: DBDep,
        current_user: UserDep,
):
    try:
        chat_previews = await db.chats.get_chats_by_user_id(current_user.id)

        return ChatsList(chats=chat_previews)

    except DBException as e:
        # Log the exception `e`
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve chat list., {e}"
        )

class ChatCreateRequest(BaseModel):
    user_ids: list[UUID]

    @field_validator('user_ids')
    @classmethod
    def validate_users(cls, v):
        if len(v) != 2:
            raise ValueError('A chat must be between exactly 2 users.')
        if len(set(v)) != len(v):
            raise ValueError('User IDs must be unique.')
        return v


@router.post("/chats", response_model=str, tags=["Chat"],
             summary="Create a new chat")
async def post_chat(
        chat_request: ChatCreateRequest,
        db: DBDep,
):
    try:
        chat_id = await db.chats.post_chat(chat_request.user_ids)

        return chat_id

    except DBException as e:
        # Log the exception `e`
        raise HTTPException(
            status_code=500, detail=f"Failed to post chat., {e}"
        )
