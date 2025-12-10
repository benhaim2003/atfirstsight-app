from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from atfirstsight_api.db.exceptions import ItemNotFoundException, DuplicateItemException


async def item_not_found_exception_handler(_: Request, exc: ItemNotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def duplicate_item_exception_handler(_: Request, exc: DuplicateItemException) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ItemNotFoundException, item_not_found_exception_handler)
    app.add_exception_handler(DuplicateItemException, duplicate_item_exception_handler)
