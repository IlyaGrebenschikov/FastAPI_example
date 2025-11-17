from pydantic import BaseModel

class BaseDoc(BaseModel):
    message: str


class UnAuthorizedError(BaseDoc): ...


class NotFoundError(BaseDoc): ...


class BadRequestError(BaseDoc): ...


class TooManyRequestsError(BaseDoc): ...


class ServiceUnavailableError(BaseDoc): ...


class ForbiddenError(BaseDoc): ...


class ServiceNotImplementedError(BaseDoc): ...


class ConflictError(BaseDoc): ...
