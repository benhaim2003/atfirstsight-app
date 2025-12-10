import hashlib
import os
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends

from atfirstsight_api.api.dependencies.auth import UserDep, get_user
from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.api.dependencies.storage import StorageDep
from atfirstsight_api.api.api_models.profiles import ProfileCreate
from atfirstsight_api.models.profiles import Profile, ProfileStatus, ProfilePhoto
from atfirstsight_api.storage.storage import PROFILE_PHOTOS_BUCKET

router = APIRouter(prefix="/profiles", tags=["profiles"], dependencies=[Depends(get_user)])


async def get_profile(profile_id: UUID, db: DBDep) -> Profile:
    return await db.profiles.get_profile(profile_id)


ProfileDep = Annotated[Profile, Depends(get_profile)]


@router.get("/{profile_id}")
async def get_profile(profile: ProfileDep) -> Profile:
    return profile


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
    file_hash = await _get_file_hash(file)
    file_extension = os.path.splitext(file.filename)[1]
    storage_path = f"{profile.id}-{file_hash}{file_extension}"
    await storage.upload_file(
        PROFILE_PHOTOS_BUCKET,
        storage_path,
        file.file.read(),
        file.content_type
    )
    await db.profiles.insert_profile_photo(
        profile.id,
        ProfilePhoto(storage_path=storage_path, sort_order=len(profile.photos) + 1)
    )


@router.delete("/{profile_id}/photos/{profile_photo_id}")
async def delete_profile_photo(
        profile_photo_id: UUID,
        _: ProfileDep,
        db: DBDep,
        storage: StorageDep,
) -> None:
    profile_photo = await db.profiles.get_profile_photo(profile_photo_id)
    await db.profiles.delete_profile_photo(profile_photo_id)
    await storage.delete_file(PROFILE_PHOTOS_BUCKET, profile_photo.storage_path)


async def _get_file_hash(file: UploadFile) -> str:
    h = hashlib.new("sha256")
    h.update(await file.read())
    return h.hexdigest()
