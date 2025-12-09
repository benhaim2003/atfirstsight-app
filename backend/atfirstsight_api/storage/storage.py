from io import BytesIO

from supabase import AsyncClient

PROFILE_PHOTOS_BUCKET = "profile_photos"

class Storage:
    def __init__(self, supabase_client: AsyncClient) -> None:
        self._supabase_client = supabase_client

    async def upload_file(self, bucket: str, destination: str, file: bytes, content_type: str) -> None:
        await self._supabase_client.storage.from_(bucket).upload(
            destination,
            file,
            file_options={"content-type": content_type}
        )
