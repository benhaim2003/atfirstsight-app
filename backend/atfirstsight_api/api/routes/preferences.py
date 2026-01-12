from datetime import datetime

from fastapi import APIRouter, Depends

from atfirstsight_api.api.api_models.preferences import ProfilePreferencesCreate
from atfirstsight_api.api.dependencies.auth import UserDep, get_user
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.models.preferences import ProfilePreferences

router = APIRouter(prefix="/preferences", tags=["preferences"], dependencies=[Depends(get_user)])


@router.get("", summary="Get a user his profile preferences")
async def get_profile_preference(
        db: DBDep,
        current_user: UserDep
) -> ProfilePreferences:
    profile_preference = await db.preferences.get_profile_preferences(current_user.id)
    return profile_preference


@router.post("", summary="Insert or Update for a user his profile preferences")
async def insert_profile_preference(
        db: DBDep,
        current_user: UserDep,
        profile_preference_create: ProfilePreferencesCreate
) -> None:
    profile_preference = ProfilePreferences(
        created_at=datetime.now(),
        profile_id=current_user.id,
        min_age=profile_preference_create.min_age,
        max_age=profile_preference_create.max_age,
        gender_pref=profile_preference_create.gender_pref
    )
    await db.preferences.insert_profile_preferences(profile_preference)

# TODO: check with Dan and Gal if there are other routes they thinks fit preferences:
#  reset_preferences (Resets the user's preferences to system defaults (e.g., Age 18-99, All Genders))
#  validate_compatibility (Checks if a specific other user (target_user_id) matches the current user's preferences)
#  get_preference_stats (Returns a count of how many potential matches exist with the current preferences)
