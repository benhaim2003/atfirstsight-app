from asyncpg import Connection

from atfirstsight_api.db.profiles_repo import ProfilesRepo
from atfirstsight_api.db.chat_repo import ChatsRepo
from atfirstsight_api.db.approach_requests_repo import ApproachesRepo


class DB:
    def __init__(self, connection: Connection) -> None:
        self.profiles = ProfilesRepo(connection)
        self.chats = ChatsRepo(connection)
        self.approaches = ApproachesRepo(connection)
