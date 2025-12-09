from contextlib import asynccontextmanager
from typing import Generator
from supabase import create_async_client
import asyncpg
from fastapi import FastAPI

from atfirstsight_api.db.db import DB
from atfirstsight_api.settings import settings
from atfirstsight_api.storage.storage import Storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator[None, None, None]:
    connection = await asyncpg.connect(settings.postgres_connection_string, statement_cache_size=0)
    app.state.db = DB(connection)

    supabase_client = await create_async_client(settings.supabase.url, settings.supabase.service_key)
    app.state.storage = Storage(supabase_client)
    yield
