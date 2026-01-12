import json
from uuid import UUID

from asyncpg import Connection, PostgresError

from atfirstsight_api.db.exceptions import ItemNotFoundException, DBException
from atfirstsight_api.models.preferences import ProfilePreferences


class PreferencesRepo:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def get_profile_preferences(self, profile_id: UUID) -> ProfilePreferences:
        try:
            profile_preferences_row = await self._connection.fetchrow(
                """
                SELECT * FROM public.profile_preferences WHERE profile_id = $1
                """,
                profile_id
            )
            if not profile_preferences_row:
                raise ItemNotFoundException(f"Profile preferences with profile id: '{profile_id}' not found")

            return ProfilePreferences.model_validate(dict(profile_preferences_row))

        except PostgresError as e:
            raise DBException(f"Failed getting {profile_id} profile preferences from db") from e

    async def insert_profile_preferences(self, profile_preferences: ProfilePreferences) -> None:
        gender_pref_json = None
        if profile_preferences.gender_pref:
            gender_pref_json = json.dumps([g.value for g in profile_preferences.gender_pref])

        try:
            await self._connection.execute(
                """
                INSERT INTO public.profile_preferences
                    (created_at, profile_id, min_age, max_age, gender_pref)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (profile_id)
                DO UPDATE SET
                    min_age = EXCLUDED.min_age,
                    max_age = EXCLUDED.max_age,
                    gender_pref = EXCLUDED.gender_pref
                """,
                profile_preferences.created_at,
                profile_preferences.profile_id,
                profile_preferences.min_age,
                profile_preferences.max_age,
                gender_pref_json
            )

        except PostgresError as e:
            raise DBException(f"Failed inserting {profile_preferences.profile_id} profile preferences to db") from e