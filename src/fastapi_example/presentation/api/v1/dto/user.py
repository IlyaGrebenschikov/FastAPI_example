from .base import BaseSchema


class CreateUserDTO(BaseSchema):
    username: str
    email: str
    password: str