class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    def get_dict(self) -> dict:
        return self.__dict__


class UnAuthorizedException(CustomException):
    pass


class ConflictException(CustomException):
    pass


class NotFoundException(CustomException):
    pass


class DatabaseError(Exception):
    pass


class CommitError(DatabaseError):
    pass


class RollbackError(DatabaseError):
    pass


class InvalidParamsError(DatabaseError):
    pass
