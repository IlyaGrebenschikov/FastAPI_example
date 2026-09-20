from typing import Any


class AppException(Exception):
    def __init__(
        self,
        message: str = "App exception",
        headers: dict[str, Any] | None = None,
    ) -> None:
        self.content = {"message": message}
        self.headers = headers

    def as_dict(self) -> dict[str, Any]:
        return {"content": self.content, "headers": self.headers}


class DetailedError(AppException):
    def __init__(
        self,
        message: str,
        headers: dict[str, Any] | None = None,
        **additional: Any,
    ) -> None:
        super().__init__(message=message, headers=headers)
        self.content |= additional

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.content}\nHeaders: {self.headers or ''}"


class UnAuthorizedError(DetailedError): ...


class NotFoundError(DetailedError): ...


class BadRequestError(DetailedError): ...


class TooManyRequestsError(DetailedError): ...


class ServiceUnavailableError(DetailedError): ...


class ForbiddenError(DetailedError): ...


class ServiceNotImplementedError(DetailedError): ...


class ConflictError(DetailedError): ...
