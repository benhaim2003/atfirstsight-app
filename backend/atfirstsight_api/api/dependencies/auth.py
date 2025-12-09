from typing import Annotated

import aiohttp
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from atfirstsight_api.api.dependencies.db import DBDep
from atfirstsight_api.db.exceptions import ItemNotFoundException
from atfirstsight_api.models.profiles import Profile
from atfirstsight_api.models.users import User
from atfirstsight_api.settings import settings

security = HTTPBearer()


async def get_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Authorization scheme is not Bearer")

    headers = {
        "Authorization": f"Bearer {credentials.credentials}",
        "apikey": settings.supabase.anon_key,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.supabase.url}/auth/v1/user", headers=headers) as response:
                response.raise_for_status()
                return User.model_validate(await response.json())

    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            raise HTTPException(status_code=401, detail=f"Unauthorized")
        raise
    except aiohttp.ClientError:
        raise HTTPException(status_code=500, detail="Failed validating user authorization")


UserDep = Annotated[User, Depends(get_user)]


async def get_profile(
        profile_id: str,
        user: UserDep,
        db: DBDep
) -> Profile:
    try:
        return await db.profiles.get_profile(profile_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail=f"profile with id: '{user.id}' not found")


ProfileDep = Annotated[Profile, Depends(get_profile)]
