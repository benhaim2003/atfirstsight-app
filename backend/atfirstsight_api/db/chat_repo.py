import uuid
from datetime import datetime
from uuid import UUID

from asyncpg import Connection
from asyncpg.exceptions import PostgresError
from pydantic import TypeAdapter

from atfirstsight_api.api.api_models.chats import CreateMessageRequest
from atfirstsight_api.db.exceptions import (DBException, ItemNotFoundException, AccessDeniedException)
from atfirstsight_api.models.chats import Chat, ChatParticipant, Message, ChatsListItem


class ChatsRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_chats_by_user_id(self, user_id: UUID) -> list[ChatsListItem]:
        chats_list_query = """
                           WITH user_chats AS (SELECT id      as chat_id,
                                                      CASE
                                                          WHEN profile_a_id = $1 THEN profile_b_id
                                                          ELSE profile_a_id
                                                          END as profile_b_id,
                                                      created_at,
                                                      updated_at
                                               FROM public.chats
                                               WHERE profile_a_id = $1
                                                  OR profile_b_id = $1),
                                latest_message AS (SELECT *
                                                   FROM (SELECT *,
                                                                ROW_NUMBER() OVER(PARTITION BY chat_id ORDER BY created_at DESC) as rn
                                                         FROM public.messages
                                                         WHERE chat_id IN (SELECT chat_id FROM user_chats)) as ranked_messages
                                                   WHERE rn = 1)

                           SELECT uc.chat_id,
                                  uc.created_at,
                                  uc.updated_at,
                                  p.id            as other_profile_id,
                                  p.username      as other_username,
                                  pp.storage_path as other_primary_photo_url,
                                  lm.id           as last_message_id,
                                  lm.sender_id    as last_message_sender_id,
                                  lm.content      as last_message_content,
                                  lm.created_at   as last_message_created_at,
                                  lm.read_at      as last_message_read_at,
                                  lm.msg_type     as last_message_msg_type,
                                  lm.metadata     as last_message_metadata
                           FROM user_chats uc
                                    LEFT JOIN public.profiles p
                                              ON uc.profile_b_id = p.id
                                    LEFT JOIN latest_message lm
                                              ON uc.chat_id = lm.chat_id
                               --TODO: make sure each profile has at most 1 profile_photo or use LATERAL JOIN
                                    LEFT JOIN public.profile_photo pp
                                              ON p.id = pp.profile_id
                           ORDER BY lm.created_at DESC NULLS LAST; \
                           """

        user_profile_query = """
                             SELECT p.id,
                                    p.username,
                                    pp.storage_path
                             FROM public.profiles p
                                      LEFT JOIN public.profile_photo pp
                                                on p.id = pp.profile_id
                             WHERE p.id = $1 \
                             """

        try:
            participant_a_data = await self._connection.fetchrow(user_profile_query, user_id)
            participant_a_dict = dict(participant_a_data)
            participant_a = ChatParticipant(
                profile_id=participant_a_dict['id'],
                username=participant_a_dict['username'],
                primary_photo_url=participant_a_dict.get('storage_path')
            )

            rows = await self._connection.fetch(chats_list_query, user_id)
            chat_previews = []
            for row in rows:
                row_dict = dict(row)

                participant_b = ChatParticipant(
                    profile_id=row_dict['other_profile_id'],
                    username=row_dict['other_username'],
                    primary_photo_url=row_dict.get('other_primary_photo_url')
                )

                chat = Chat(
                    id=row_dict['chat_id'],
                    participant_a=participant_a,
                    participant_b=participant_b,
                    created_at=row_dict['created_at'],
                    updated_at=row_dict['updated_at']
                )

                if row_dict.get('last_message_id'):
                    last_message = Message(
                        id=row_dict['last_message_id'],
                        chat_id=row_dict['chat_id'],
                        sender_id=row_dict['last_message_sender_id'],
                        content=row_dict['last_message_content'],
                        created_at=row_dict['last_message_created_at'],
                        read_at=row_dict.get('last_message_read_at'),
                        msg_type=row_dict['last_message_msg_type'],
                        metadata=row_dict.get('last_message_metadata')
                    )
                else:
                    last_message = None

                chat_previews.append(
                    ChatsListItem(
                        chat=chat,
                        last_message=last_message
                    )
                )

            return chat_previews

        except PostgresError as e:
            raise DBException(f"Failed getting chat list from db, {e}") from e

    async def insert_chat(self, users_ids: list[UUID]) -> UUID:
        insert_chat_query = """
                          WITH ins AS (
                          INSERT
                          INTO public.chats (profile_a_id, profile_b_id)
                          VALUES ($1, $2)
                          ON CONFLICT (profile_a_id, profile_b_id) DO NOTHING
                              RETURNING id
                              )
                          SELECT id
                          FROM ins
                          UNION ALL
                          SELECT id
                          FROM public.chats
                          WHERE profile_a_id = $1
                            AND profile_b_id = $2 LIMIT 1;
                          """

        users_ids = sorted(users_ids)
        user_a_id = users_ids[0]
        user_b_id = users_ids[1]

        try:
            chat_id = await self._connection.fetchval(insert_chat_query, user_a_id, user_b_id)
            return chat_id
        except PostgresError as e:
            raise DBException(f"Failed creating chat in db, {e}") from e

    async def get_chat(self, chat_id: UUID, user_id: UUID) -> Chat | None:
        get_chat_query = """
                         SELECT c.id            as chat_id
                              , c.created_at
                              , c.updated_at
                              , p.id            as profile_id
                              , p.username
                              , pp.storage_path as primary_photo_url
                         FROM public.chats c
                                  JOIN public.profiles p
                                       ON p.id IN (c.profile_a_id, c.profile_b_id)
                             --TODO: make sure each profile has at most 1 profile_photo or use LATERAL JOIN
                                  LEFT JOIN profile_photos pp
                                            ON pp.profile_id = p.id
                         WHERE c.id = $1 and (c.profile_a_id = $2 or c.profile_b_id = $2)
                         """
        try:
            rows = await self._connection.fetch(get_chat_query, chat_id, user_id)
            if not rows:
                raise ItemNotFoundException(f"Chat with id {chat_id} not found.")

            participant_a = None
            participant_b = None

            chat_created_at = rows[0]['created_at']
            chat_updated_at = rows[0]['updated_at']

            for row in rows:
                row_dict = dict(row)
                if user_id == row_dict.get('profile_id'):
                    participant_a = ChatParticipant(
                        profile_id=row_dict['profile_id'],
                        username=row_dict['username'],
                        primary_photo_url=row_dict.get('primary_photo_url')
                    )
                else:
                    # TODO: think what should happened if profile_b has been deleted (should the chat be deleted too?) should we add an "is active" to profiles to not delete them even if a profile got deleted?
                    participant_b = ChatParticipant(
                        profile_id=row_dict['profile_id'],
                        username=row_dict['username'],
                        primary_photo_url=row_dict.get('primary_photo_url')
                    )

            chat = Chat(
                id=chat_id,
                participant_a=participant_a,
                participant_b=participant_b,
                created_at=chat_created_at,
                updated_at=chat_updated_at
            )

            return chat

        except PostgresError as e:
            raise DBException(f"Failed getting chat from db, {e}") from e


    async def get_chat_messages(self, chat_id: UUID, user_id: UUID, limit: int, skip: int) -> list[Message]:
        query = """
                SELECT id, \
                       chat_id, \
                       sender_id, \
                       content, \
                       msg_type, \
                       metadata, \
                       created_at, \
                       read_at
                FROM public.messages
                WHERE chat_id = $1
                ORDER BY created_at DESC
                    LIMIT $2 \
                OFFSET $3; \
                """
        try:
            if not self._user_is_participant(chat_id, user_id):
                raise ItemNotFoundException(f"Chat with id {chat_id} not found.")

            rows = await self._connection.fetch(query, chat_id, limit, skip)
            return [Message.model_validate(dict(r)) for r in rows]

        except PostgresError as e:
            raise DBException(f"Failed getting chat from db, {e}") from e


    async def insert_chat_messages(self, message_payload: Message) -> UUID:
        insert_chat_massage_query = """
                                    INSERT INTO public.messages (
                                        id, chat_id, sender_id, content, msg_type, metadata, created_at, read_at
                                    )
                                    VALUES (
                                        $1, $2, $3, $4, $5, $6, $7, $8
                                    )
                                    RETURNING id;
                                """
        try:
            if not self._user_is_participant(message_payload.chat_id, message_payload.sender_id):
                raise ItemNotFoundException(f"Chat with id {message_payload.chat_id} not found.")

            await self._connection.fetchval(insert_chat_massage_query, message_payload.id, message_payload.chat_id,
                                                      message_payload.sender_id, message_payload.content,
                                                      message_payload.msg_type, message_payload.metadata,
                                                      message_payload.created_at, message_payload.read_at)
            return message_payload.id
        except PostgresError as e:
            raise DBException(f"Failed creating chat in db, {e}") from e


    async def _user_is_participant(self, chat_id: UUID, user_id: UUID) -> bool:
        check_query = """
                      SELECT EXISTS(SELECT 1
                                    FROM public.chats
                                    WHERE id = $1 AND (profile_a_id = $2 or profile_b_id = $2)) as is_participant
                      """
        try:
            return await self._connection.fetchval(check_query, chat_id, user_id)
        except PostgresError as e:
            raise DBException(f"Failed checking if {user_id} is participant in {chat_id} chat, {e}") from e
