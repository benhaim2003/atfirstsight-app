import os
import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, APIRouter, Query, Depends, File, UploadFile

from atfirstsight_api.api.api_models.chats import CreateMessageRequest
from atfirstsight_api.api.dependencies.auth import UserDep, get_user
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.api.dependencies.storage import StorageDep
from atfirstsight_api.api.routes.profiles import _get_file_hash
from atfirstsight_api.db.exceptions import DBException
from atfirstsight_api.models.chats import ChatsList, Chat, Message
from atfirstsight_api.storage.storage import PHOTO_MESSAGES_BUCKET, AUDIO_MESSAGE_BUCKET

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
async def upload_chat(
        target_id: UUID,
        db: DBDep,
        current_user: UserDep,
) -> UUID:
    if target_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot create a chat with yourself."
        )

    approach_status = await db.approaches.get_approach_by_users_ids(
        user_a=current_user.id,
        user_b=target_id,
    )
    if approach_status != 'verified':
        raise HTTPException(
            status_code=403,
            detail="You cannot start a chat without a real meeting experience."
        )

    chat_participants = [current_user.id, target_id]
    chat_id = await db.chats.insert_chat(chat_participants)
    return chat_id


@router.get("/{chat_id}", summary="Get specific chat details")
async def get_chat(
        chat_id: UUID,
        db: DBDep,
        current_user: UserDep,
) -> Chat:
    chat = await db.chats.get_chat(chat_id, current_user.id)
    return chat


@router.get("/{chat_id}/messages", summary="Get specific chat messages")
async def get_chat_messages(
        chat_id: UUID,
        db: DBDep,
        current_user: UserDep,
        limit: int = Query(50, le=100),
        skip: int = 0
) -> list[Message]:
    messages = await db.chats.get_chat_messages(
        chat_id=chat_id,
        user_id=current_user.id,
        limit=limit,
        skip=skip
    )

    return messages


@router.post("/{chat_id}/messages", summary="Post a message to a chat")
async def upload_chat_message(
        chat_id: UUID,
        message_data: CreateMessageRequest,
        db: DBDep,
        current_user: UserDep,
        storage: StorageDep,
        file: UploadFile = File(...) | None
) -> None:
    bucket = None
    storage_path = None
    file_content = None
    file_content_type = None
    if file:
        file_content = await file.read()
        file_hash = await _get_file_hash(file_content)
        file_extension = os.path.splitext(file.filename)[1]
        storage_path = f"{chat_id}/{file_hash}{file_extension}"
        file_content_type = file.content_type
        if file_content_type.startswith("image/"):
            bucket = PHOTO_MESSAGES_BUCKET
        elif file_content_type.startswith("audio/"):
            bucket = AUDIO_MESSAGE_BUCKET
        else:
            raise HTTPException(
                status_code=415,
                detail="You cannot upload a non-image or non-audio file."
            )
        message_data.content = storage_path
    whole_message_data = Message(
    id=uuid.uuid4(),
    chat_id=chat_id,
    sender_id=current_user.id,
    created_at=datetime.now(),
    read_at=None,
    **message_data.model_dump(exclude_none=True))
    await db.chats.insert_chat_messages(
        whole_message_data
    )
    if file:
        try:
            await storage.upload_file(
                bucket,
                storage_path,
                file_content,
                file_content_type
            )
        except Exception as e:
            await db.chats.delete_chat_message(whole_message_data.id, current_user.id)
            raise HTTPException(status_code=500, detail="File upload failed") from e


@router.delete("/{chat_id}/messages", summary="Delete a message from a chat")
async def delete_chat_message(
        message_id: UUID,
        db: DBDep,
        current_user: UserDep,
) -> None:
    await db.chats.delete_chat_message(message_id, current_user.id)
