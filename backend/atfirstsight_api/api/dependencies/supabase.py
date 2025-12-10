from typing import Annotated

from fastapi import Request, Depends
from supabase import AsyncClient

from atfirstsight_api.storage.storage import Storage


def get_supabase(request: Request) -> Storage:
    return request.app.state.supabase


SupabaseDep = Annotated[AsyncClient, Depends(get_supabase)]
