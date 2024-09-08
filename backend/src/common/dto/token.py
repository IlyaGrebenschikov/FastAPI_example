from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class TokenSubject(BaseModel):
    sub: int
    scopes: list[str]
