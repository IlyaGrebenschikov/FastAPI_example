class DatabaseError(Exception):
    def __init__(self, message: str, operation: str | None = None) -> None:
        super().__init__(message)
        self.operation = operation


class CommitError(DatabaseError):
    def __init__(self, original_error: Exception | None = None) -> None:
        message = "Failed to commit transaction"
        if original_error:
            message += f": {original_error}"
        super().__init__(message, operation="commit")


class RollbackError(DatabaseError):
    def __init__(self, original_error: Exception | None = None) -> None:
        message = "Failed to rollback transaction"
        if original_error:
            message += f": {original_error}"
        super().__init__(message, operation="rollback")


class InvalidParamsError(DatabaseError):
    def __init__(self, message: str) -> None:
        super().__init__(message, operation="invalid_params")
