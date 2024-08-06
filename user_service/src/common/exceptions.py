class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    def get_dict(self) -> dict:
        return self.__dict__


class InvalidTokenException(CustomException):
    pass
