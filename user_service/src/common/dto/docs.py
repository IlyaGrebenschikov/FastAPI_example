from pydantic import BaseModel


class BaseDoc(BaseModel):
    message: str


class ConflictError(BaseDoc):
    pass


class NotFoundError(BaseDoc):
    pass


class BadRequestError(BaseDoc):
    pass
