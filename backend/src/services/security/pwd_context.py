from passlib.context import CryptContext


def get_pwd_context(hashing_algorithms: list[str]) -> CryptContext:
    return CryptContext(schemes=hashing_algorithms, deprecated="auto")
