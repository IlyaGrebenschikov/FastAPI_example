from typing import TypedDict, NotRequired

class UpdateUserType(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]


class CreateUserType(TypedDict):
    username: str
    email: str
    password: str
