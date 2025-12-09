from typing import Annotated

from fastapi import Request, Depends

from atfirstsight_api.storage.storage import Storage


def get_storage(request: Request) -> Storage:
    return request.app.state.storage


StorageDep = Annotated[Storage, Depends(get_storage)]
