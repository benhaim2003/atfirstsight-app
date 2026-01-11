from supabase import AsyncClient
from supabase import StorageException as SupabaseStorageException

from atfirstsight_api.storage.exceptions import StorageException

PROFILE_PHOTOS_BUCKET = "profile_photos"
PHOTO_MESSAGES_BUCKET = "photos_massages"
AUDIO_MESSAGE_BUCKET = "audio_messages"

class Storage:
    def __init__(self, supabase_client: AsyncClient) -> None:
        self._supabase_client = supabase_client

    async def upload_file(self, bucket: str, destination: str, file: bytes, content_type: str) -> None:
        try:
            await self._supabase_client.storage.from_(bucket).upload(
                destination,
                file,
                file_options={"content-type": content_type}
            )
        except SupabaseStorageException as e:
            raise StorageException("Failed uploading file") from e

    async def delete_file(self, bucket: str, path: str) -> None:
        try:
            await self._supabase_client.storage.from_(bucket).remove(path)
        except SupabaseStorageException as e:
            raise StorageException("Failed deleting file") from e