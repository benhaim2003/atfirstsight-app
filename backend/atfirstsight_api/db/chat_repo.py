from uuid import UUID

from asyncpg import Connection
from asyncpg.exceptions import PostgresError, UniqueViolationError
# Make sure your custom exceptions are importable
from atfirstsight_api.db.exceptions import (DBException,
                                            DuplicateItemException,
                                            ItemNotFoundException)
from atfirstsight_api.models.chat import Chat, Message
from atfirstsight_api.models.chats import (ChatParticipant, ChatPreview,
                                           LastMessage)


class ChatsRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_chat_by_id(self, chat_id: UUID) -> Chat:
        """Fetches a single chat room by its ID."""
        try:
            chat_row = await self._connection.fetchrow(
                """
                SELECT * FROM public.chats
                WHERE id = $1
                """,
                chat_id,
            )
            if not chat_row:
                raise ItemNotFoundException(f"Chat with id: '{chat_id}' not found")

            # Chat model is a flat structure, so we can validate directly
            return Chat.model_validate(dict(chat_row))

        except PostgresError as e:
            raise DBException("Failed getting chat from db") from e

    async def get_messages_by_chat_id(
        self, chat_id: UUID, limit: int = 50
    ) -> list[Message]:
        """Fetches the N most recent messages for a chat."""
        try:
            message_rows = await self._connection.fetch(
                """
                SELECT * FROM public.messages
                WHERE chat_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                chat_id,
                limit,
            )

            # We fetch newest-first (DESC), but the UI needs oldest-first.
            # We reverse the list before validating.
            return [
                Message.model_validate(dict(row)) for row in reversed(message_rows)
            ]

        except PostgresError as e:
            raise DBException("Failed getting messages from db") from e

    # NEW, MODIFIED code
    async def insert_message(self, message: Message) -> Message:
        """
        Inserts a new message into the database and
        returns the newly created message.
        """
        try:
            new_row = await self._connection.fetchrow( # <-- 1. Use fetchrow
                """
                INSERT INTO public.messages
                (id, chat_id, sender_id, content, created_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *; 
                """, # <-- 2. Added RETURNING *
                message.id,
                message.chat_id,
                message.sender_id,
                message.content,
                message.created_at,
            )
            if not new_row:
                raise DBException("Failed to create message, no row returned")
            
            # 3. Validate and return the new message
            return Message.model_validate(dict(new_row))

        except UniqueViolationError as e:
            raise DuplicateItemException(
                f"Duplicate message id: '{message.id}'"
            ) from e
        except PostgresError as e:
            raise DBException("Failed inserting message to db") from e
    
    async def get_chats_by_user_id(self, user_id: UUID) -> list[ChatPreview]:
        """
        Fetches all chat previews for a given user, including the
        other participant's details and the last message sent.
        """
        
        # This query does all the work:
        # 1. Finds all chats for the user.
        # 2. Identifies the "other" participant's ID.
        # 3. Joins with `profiles` to get the other participant's details.
        # 4. Uses a `LEFT JOIN` on a subquery to get the *last message* for each chat.
        sql_query = """
        WITH user_chats AS (
            -- 1. Find all chats for the current user and identify the "other" profile
            SELECT
                id as chat_id,
                CASE
                    WHEN profile_a_id = $1 THEN profile_b_id
                    ELSE profile_a_id
                END as other_participant_id
            FROM public.chats
            WHERE profile_a_id = $1 OR profile_b_id = $1
        ),
        latest_message AS (
            -- 2. Find the last message for each chat
            SELECT
                chat_id,
                content,
                created_at,
                sender_id
            FROM (
                SELECT
                    chat_id,
                    content,
                    created_at,
                    sender_id,
                    ROW_NUMBER() OVER(PARTITION BY chat_id ORDER BY created_at DESC) as rn
                FROM public.messages
                WHERE chat_id IN (SELECT chat_id FROM user_chats)
            ) as ranked_messages
            WHERE rn = 1
        )
        -- 3. Join everything together
        SELECT
            uc.chat_id,
            p.id as other_profile_id,
            p.username as other_username,
            lm.content as last_message_content,
            lm.created_at as last_message_created_at,
            lm.sender_id as last_message_sender_id
        FROM user_chats uc
        LEFT JOIN public.profiles p ON uc.other_participant_id = p.id
        LEFT JOIN latest_message lm ON uc.chat_id = lm.chat_id
        ORDER BY lm.created_at DESC NULLS LAST; -- Show newest chats first
        """

        try:
            rows = await self._connection.fetch(sql_query, user_id)

            chat_previews = []
            for row in rows:
                # We need to manually construct the nested Pydantic models
                # from the flat SQL row (as a dict)
                row_dict = dict(row)
                
                other_participant = ChatParticipant(
                    profile_id=row_dict.get('other_profile_id'),
                    username=row_dict.get('other_username'),
                )

                last_message = None
                if row_dict.get('last_message_content'):
                    last_message = LastMessage(
                        content=row_dict.get('last_message_content'),
                        created_at=row_dict.get('last_message_created_at'),
                        sender_id=row_dict.get('last_message_sender_id')
                    )

                chat_previews.append(
                    ChatPreview(
                        chat_id=row_dict.get('chat_id'),
                        other_participant=other_participant,
                        last_message=last_message,
                        unread_count=0  # Stubbed for now
                    )
                )

            return chat_previews

        except PostgresError as e:
            # You should log the error `e` here
            raise DBException(f"Failed getting chat list from db, {e}") from e