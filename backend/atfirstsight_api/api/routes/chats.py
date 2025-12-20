from uuid import UUID

from fastapi import HTTPException, APIRouter

from atfirstsight_api.api.dependencies.auth import UserDep
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.db.exceptions import DBException
from atfirstsight_api.models.chats import ChatsList, Chat

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


@router.post("/chats", response_model=UUID, tags=["Chat"],
             summary="Create a new chat")
async def post_chat(
        target_id: UUID,
        db: DBDep,
        current_user: UserDep,
):
    if target_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot create a chat with yourself."
        )

    approach_status = await db.approaches.check_approach_status(
        user_a=current_user.id,
        user_b=target_id,
    )
    if approach_status != 'verified':
        raise HTTPException(
            status_code=403,
            detail="You cannot start a chat without a real meeting experience."
        )

    chat_participants = [current_user.id, target_id]
    try:
        chat_id = await db.chats.post_chat(chat_participants)

        return chat_id

    except DBException as e:
        # Log the exception `e`
        raise HTTPException(
            status_code=500, detail=f"Failed to post chat., {e}"
        )


@router.get("/chats/{chat_id}", response_model=Chat, tags=["Chat"],
            summary="Get specific chat details")
async def get_chat(
        chat_id: UUID,
        db: DBDep,
        current_user: UserDep,
):
    try:
        chat = await db.chats.get_chat(chat_id, current_user.id)

        return chat

    except DBException as e:
        # Log the exception `e`
        raise HTTPException(
            status_code=500, detail=f"Failed to get chat., {e}"
        )
