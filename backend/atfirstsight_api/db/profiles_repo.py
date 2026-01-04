from uuid import UUID

from asyncpg import Connection
from asyncpg.exceptions import PostgresError, UniqueViolationError

from atfirstsight_api.db.exceptions import ItemNotFoundException, DBException, DuplicateItemException
from atfirstsight_api.models.profiles import Profile, ProfilePhoto


class ProfilesRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_profile(self, profile_id: str) -> Profile:
        try:
            profile_row = await self._connection.fetchrow(
                """
                SELECT * FROM public.profiles
                WHERE id = $1
                """,
                profile_id
            )
            if not profile_row:
                raise ItemNotFoundException(f"Profile with id: '{profile_id}' not found")

            profile_photo_rows = await self._connection.fetch(
                """
                SELECT * FROM public.profile_photos
                WHERE profile_id = $1
                """,
                profile_id
            )

            return Profile.model_validate(
                {**profile_row, "photos": [dict(profile_photo_row) for profile_photo_row in profile_photo_rows]})
        except PostgresError as e:
            raise DBException("Failed getting profile from db") from e

    async def get_profile_photo(self, profile_photo_id: UUID) -> ProfilePhoto:
        try:
            profile_photo_row = await self._connection.fetchrow(
                """
                SELECT * FROM public.profile_photos
                WHERE id = $1
                """,
                profile_photo_id
            )
            if not profile_photo_row:
                raise ItemNotFoundException(f"Profile photo with id: '{profile_photo_id}' not found")

            return ProfilePhoto.model_validate(dict(profile_photo_row))

        except PostgresError as e:
            raise DBException("Failed getting profile photo from db") from e

    async def insert_profile(self, profile: Profile) -> None:
        try:
            await self._connection.execute(
                """
                INSERT INTO public.profiles
                (id, username, bio, gender, birth_date, status)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                profile.id,
                profile.username,
                profile.bio,
                profile.gender,
                profile.birth_date,
                profile.status,
            )

        except UniqueViolationError as e:
            raise DuplicateItemException(f"duplicate profile id: '{profile.id}'") from e
        except PostgresError as e:
            raise DBException("Failed inserting profile to db") from e

    async def insert_profile_photo(
            self, profile_id: UUID, profile_photo: ProfilePhoto
    ) -> None:
        try:
            await self._connection.execute(
                """
                INSERT INTO public.profile_photos
                (id, profile_id, storage_path, sort_order, uploaded_at)
                VALUES ($1, $2, $3, $4, $5)
                """,
                profile_photo.id,
                profile_id,
                profile_photo.storage_path,
                profile_photo.sort_order,
                profile_photo.uploaded_at
            )
        except UniqueViolationError as e:
            raise DuplicateItemException(f"duplicate profile photo id: '{profile_photo.id}'") from e
        except PostgresError as e:
            raise DBException("Failed inserting profile photo to db") from e

    async def delete_profile_photo(self, profile_photo_id: UUID) -> None:
        try:
            await self._connection.execute(
                """
                DELETE FROM public.profile_photos
                WHERE id = $1
                """,
                profile_photo_id
            )
        except PostgresError as e:
            raise DBException("Failed deleting profile photo to db") from e