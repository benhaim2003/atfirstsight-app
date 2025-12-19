from uuid import UUID

from asyncpg import Connection
from asyncpg.exceptions import PostgresError

from atfirstsight_api.db.exceptions import (DBException)
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
            participant_a_data = await self._connection.fetch(user_profile_query, user_id)
            participant_a_dict = dict(participant_a_data[0])
            participant_a = ChatParticipant(
                profile_id=participant_a_dict.get('id'),
                username=participant_a_dict.get('username'),
                primary_photo_url=participant_a_dict.get('storage_path')
            )

            rows = await self._connection.fetch(chats_list_query, user_id)
            chat_previews = []
            for row in rows:
                row_dict = dict(row)

                participant_b = ChatParticipant(
                    profile_id=row_dict.get('other_profile_id'),
                    username=row_dict.get('other_username'),
                    primary_photo_url=row_dict.get('other_primary_photo_url')
                )

                chat = Chat(
                    id=row_dict.get('chat_id'),
                    participant_a=participant_a,
                    participant_b=participant_b,
                    created_at=row_dict.get('created_at'),
                    updated_at=row_dict.get('updated_at')
                )

                if row_dict.get('last_message_id'):
                    last_message = Message(
                        id=row_dict.get('last_message_id'),
                        chat_id=row_dict.get('chat_id'),
                        sender_id=row_dict.get('last_message_sender_id'),
                        content=row_dict.get('last_message_content'),
                        created_at=row_dict.get('last_message_created_at'),
                        read_at=row_dict.get('last_message_read_at'),
                        msg_type=row_dict.get('last_message_msg_type'),
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

    async def post_chat(self, users_ids: list[UUID]) -> str:
        post_chat_query = """
                            WITH ins AS (
                                INSERT INTO public.chats (profile_a_id, profile_b_id)
                                VALUES ($1, $2)
                                ON CONFLICT (profile_a_id, profile_b_id) DO NOTHING
                                RETURNING id
                            )
                            SELECT id FROM ins
                            UNION ALL
                            SELECT id FROM public.chats
                            WHERE profile_a_id = $1 AND profile_b_id = $2
                            LIMIT 1;
                          """

        users_ids = sorted(users_ids)
        user_a_id = users_ids[0]
        user_b_id = users_ids[1]

        try:
            chat_id = await self._connection.fetchval(post_chat_query, user_a_id, user_b_id)
            return str(chat_id)
        except PostgresError as e:
            raise DBException(f"Failed creating chat in db, {e}") from e
