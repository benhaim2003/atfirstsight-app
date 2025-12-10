import os
import uuid

from fastapi import APIRouter
from fastapi import UploadFile, File

from atfirstsight_api.api.dependencies.auth import UserDep, ProfileDep
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.api.dependencies.storage import StorageDep
from atfirstsight_api.api.models.profiles import ProfileCreate
from atfirstsight_api.models.profiles import Profile, ProfileStatus, ProfilePhoto
from atfirstsight_api.storage.storage import PROFILE_PHOTOS_BUCKET

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("")
async def register_profile(
        profile_create: ProfileCreate,
        user: UserDep,
        db: DBDep,
) -> None:
    profile = Profile(
        id=user.id,
        username=profile_create.username,
        bio=profile_create.bio,
        gender=profile_create.gender,
        birth_date=profile_create.birth_date,
        status=ProfileStatus.Offline,
        photos=[]
    )
    await db.profiles.insert_profile(profile)


@router.post("/{profile_id}/photo")
async def upload_profile_photo(
        profile: ProfileDep,
        db: DBDep,
        storage: StorageDep,
        file: UploadFile = File(...)
) -> None:
    storage_path = f"{profile.id}-{uuid.uuid4().hex[:4]}.{os.path.splitext(file.filename)[1]}"
    await storage.upload_file(
        PROFILE_PHOTOS_BUCKET,
        storage_path,
        file.file.read(),
        file.content_type
    )
    db.profiles.insert_profile_photo(
        profile.id,
        ProfilePhoto(storage_path=storage_path, sort_order=len(profile.photos) + 1)
    )
