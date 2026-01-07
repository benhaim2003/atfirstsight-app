from uuid import UUID

from asyncpg import Connection
from asyncpg.exceptions import PostgresError

from atfirstsight_api.db.exceptions import DBException, ItemNotFoundException


class ApproachesRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_approach_status(self, user_a: UUID, user_b: UUID) -> str | None:
        query = """
                SELECT status
                FROM public.approach_requests
                WHERE ((requester_id = $1 AND receiver_id = $2)
                    OR (requester_id = $2 AND receiver_id = $1))
                --TODO: make sure there must be only 1 approach request
                LIMIT 1;
                """
        try:
            result = await self._connection.fetchval(query, user_a, user_b)
            if result is None:
                raise ItemNotFoundException(f"No approach request found between {user_a} and {user_b}.")
            return result
        except PostgresError as e:
            raise DBException(f"Failed to check approach status between {user_a} and {user_b}: {e}") from e
