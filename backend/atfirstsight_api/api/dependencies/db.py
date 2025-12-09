from typing import Annotated

from fastapi import Request, Depends

from atfirstsight_api.db.db import DB
from atfirstsight_api.db.profiles_repo import ProfilesRepo


def get_db(request: Request) -> ProfilesRepo:
    return request.app.state.db


DBDep = Annotated[DB, Depends(get_db)]
