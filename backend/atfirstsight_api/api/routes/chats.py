from uuid import UUID

from fastapi import HTTPException, APIRouter, Query, Depends

from atfirstsight_api.api.api_models.chats import CreateMessageRequest  # Import the model above
from atfirstsight_api.api.dependencies.auth import UserDep, get_user
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.db.exceptions import DBException, AccessDenied, ItemNotFoundException
from atfirstsight_api.models.chats import ChatsList, Chat, Message

router = APIRouter(prefix="/chats", tags=["chats"], dependencies=[Depends(get_user)])


@router.get("", summary="Retrieve a list of the user's chats")
async def get_user_chat_list(
        db: DBDep,
        current_user: UserDep,
) -> ChatsList:
    try:
        chat_previews = await db.chats.get_chats_by_user_id(current_user.id)

        return ChatsList(chats=chat_previews)

    except DBException as e:
        # TODO add logs in all Exceptions
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve chat list., {e}"
        )


@router.post("", summary="Create a new chat")
async def post_chat(
        target_id: UUID,
        db: DBDep,
        current_user: UserDep,
) -> UUID:
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to post chat., {e}"
        )


@router.get("/{chat_id}", summary="Get specific chat details")
async def get_chat(
        chat_id: UUID,
        db: DBDep,
        current_user: UserDep,
) -> Chat:
    try:
        chat = await db.chats.get_chat(chat_id, current_user.id)
        return chat


    except ItemNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Chat not found")

    except AccessDenied:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this chat.")

    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get chat massages., {e}"
        )


@router.get("/{chat_id}/messages", summary="Get specific chat messages")
async def get_chat_messages(
        chat_id: UUID,
        db: DBDep,
        current_user: UserDep,
        limit: int = Query(50, le=100),
        skip: int = 0
) -> list[Message]:
    try:
        messages = await db.chats.get_chat_messages(
            chat_id=chat_id,
            user_id=current_user.id,
            limit=limit,
            skip=skip
        )

        return messages


    except ItemNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    except AccessDenied:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this chat."
        )

    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get chat massages., {e}"
        )


@router.post("/{chat_id}/messages", summary="Post a message to a chat")
async def post_chat_message(
        chat_id: UUID,
        message_data: CreateMessageRequest,
        db: DBDep,
        current_user: UserDep,
) -> UUID:
    try:
        result = await db.chats.post_chat_messages(
            chat_id=chat_id,
            sender_id=current_user.id,
            message_payload=message_data
        )

        return result

    except ItemNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Chat not found."
        )

    except AccessDenied:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to send messages in this chat."
        )

    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message., {e}"
        )
