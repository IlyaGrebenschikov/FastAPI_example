from abc import ABC, abstractmethod
from typing import Any


class AbstractHasher(ABC):
    def __init__(self, hasher: Any) -> None:
        self.hasher = hasher

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass
