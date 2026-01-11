from asyncpg import Connection
from asyncpg.exceptions import PostgresError, UniqueViolationError

from atfirstsight_api.db.exceptions import (DBException, ItemNotFoundException, DuplicateItemException)
from atfirstsight_api.models.approach_requests import ApproachRequest


class ApproachesRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_approach_request(self, approach_request_id: str) -> ApproachRequest:
        try:
            approach_request_row = await self._connection.fetchrow(
                """
                SELECT *
                FROM public.approach_requests
                WHERE id = $1
                """,
                approach_request_id
            )
            if not approach_request_row:
                raise ItemNotFoundException(f"ApproachRequest with id: '{approach_request_id}' not found")
            return ApproachRequest(**approach_request_row)
        except PostgresError as e:
            raise DBException(f"Failed getting approach request from db") from e

    async def get_approach_requests(
            self,
            receiver_id: str | None = None,
            requester_id: str | None = None
    ) -> list[ApproachRequest]:
        try:
            approach_request_rows = await self._connection.fetch(
                """
                SELECT *
                FROM public.approach_requests
                WHERE ($1::uuid IS NULL OR receiver_id = $1)
                  AND ($2::uuid IS NULL OR requester_id = $2)
                """,
                receiver_id,
                requester_id
            )
            return [ApproachRequest(**row) for row in approach_request_rows]
        except PostgresError as e:
            raise DBException(f"Failed getting approach requests from db") from e

    async def insert_approach_request(
            self, approach_request: ApproachRequest
    ) -> None:
        try:
            await self._connection.execute(
                """
                INSERT INTO public.approach_requests
                (id, receiver_id, requester_id, status, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                approach_request.id,
                approach_request.receiver_id,
                approach_request.requester_id,
                approach_request.status,
                approach_request.created_at,
                approach_request.updated_at,
            )
        except UniqueViolationError as e:
            raise DuplicateItemException(f"duplicate approach request id: '{approach_request.id}'") from e
        except PostgresError as e:
            raise DBException("Failed inserting approach request to db") from e
