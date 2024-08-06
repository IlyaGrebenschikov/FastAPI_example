from passlib.context import CryptContext

from user_service.src.common.interfaces.hasher import AbstractHasher


class BcryptHasher(AbstractHasher):
    def __init__(self, hasher: CryptContext) -> None:
        super().__init__(hasher)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.hasher.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)
