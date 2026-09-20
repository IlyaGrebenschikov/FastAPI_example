from pydantic import BaseModel


class BaseDoc(BaseModel):
    message: str


class UnauthorizedDoc(BaseDoc): ...


class NotFoundDoc(BaseDoc): ...


class BadRequestDoc(BaseDoc): ...


class TooManyRequestsDoc(BaseDoc): ...


class ServiceUnavailableDoc(BaseDoc): ...


class ForbiddenDoc(BaseDoc): ...


class ServiceNotImplementedDoc(BaseDoc): ...


class ConflictDoc(BaseDoc): ...
