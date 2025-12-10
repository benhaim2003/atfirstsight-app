import uuid

from fastapi import HTTPException, status, APIRouter

from atfirstsight_api.api.dependencies.auth import UserDep
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.api.dependencies.storage import StorageDep
from atfirstsight_api.db.exceptions import DBException
from atfirstsight_api.models.chat import ChatSession, ChatParticipant, Message, MessageCreate
from atfirstsight_api.models.chats import ChatListResponse

router = APIRouter()


@router.get("/chat_session/{chat_id}", response_model=ChatSession, tags=["Chat"])
async def get_chat_session(
        chat_id: uuid.UUID,
        user: UserDep,
        db: DBDep,
        storage: StorageDep
) -> ChatSession:
    chat = await db.chats.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if user.id not in (chat.profile_a_id, chat.profile_b_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    other_participant_id = (
        chat.profile_b_id
        if user.id == chat.profile_a_id
        else chat.profile_a_id
    )

    other_profile = await db.profiles.get_profile(other_participant_id)
    if not other_profile:
        raise HTTPException(status_code=404, detail="Participant profile not found")

    messages = await db.chats.get_messages_by_chat_id(chat_id, limit=50)

    # 6. Build the other participant's photo URL
    # primary_photo_url = None
    # if other_profile.photos:
    #     # Find the photo with sort_order 1, or fall back to the first photo
    #     primary_photo = next((p for p in other_profile.photos if p.sort_order == 1), None)
    #     if not primary_photo:
    #         primary_photo = other_profile.photos[0] # Fallback to first

    #     if primary_photo:
    #         # Assumes your storage dep can create a public URL
    #         primary_photo_url = await storage.get_public_url(
    #             PROFILE_PHOTOS_BUCKET, 
    #             primary_photo.storage_path
    #         )

    # 7. Assemble the response model
    other_participant = ChatParticipant(
        profile_id=other_profile.id,
        username=other_profile.username,
        # primary_photo_url=primary_photo_url
    )

    return ChatSession(
        chat_id=chat.id,
        other_participant=other_participant,
        messages=messages
    )


@router.get("/chats/", response_model=ChatListResponse, tags=["Chat"],
            summary="Get all chat sessions for the current user",
            )
async def get_user_chat_list(
        db: DBDep,
        current_user: UserDep,  # Get user from auth
):
    """
    Fetches a list of all active chat sessions for the authenticated user.

    Each chat preview includes:
    - The other participant's details (username, photo)
    - The last message sent in the chat
    """
    try:
        # We use the authenticated user's ID
        chat_previews = await db.chats.get_chats_by_user_id(current_user.id)

        return ChatListResponse(chats=chat_previews)

    except DBException as e:
        # Log the exception `e`
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve chat list., {e}"
        )


@router.post(
    "/chats/{chat_id}/messages",
    response_model=Message,
    status_code=status.HTTP_201_CREATED,
    tags=["Chat"],
    summary="Send a message to a chat",
)
async def send_message(
        chat_id: uuid.UUID,
        message_in: MessageCreate,  # Assuming you added this to your models
        db: DBDep,
        current_user: UserDep,
):
    chat = await db.chats.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user.id not in (chat.profile_a_id, chat.profile_b_id):
        raise HTTPException(
            status_code=403,
            detail="You are not a participant in this chat"
        )

    # 2. Build the full Message object
    message_to_db = Message(
        chat_id=chat_id,
        sender_id=current_user.id,
        content=message_in.content
    )

    try:
        # 3. Call your (now modified) repo method
        new_message = await db.chats.insert_message(message_to_db)

        # 4. Return the new message
        return new_message

    except DBException as e:
        raise HTTPException(
            status_code=500, detail="Failed to send message."
        )
