from backend.src.common.interfaces.gateway import BaseGateway
from backend.src.database.gateway import DBGateway
from backend.src.services.user import UserService


class ServiceGateway(BaseGateway):
    def __init__(self, database: DBGateway) -> None:
        self.database = database
        super().__init__(database)

    def user(self) -> UserService:
        return UserService(self.database.user())
