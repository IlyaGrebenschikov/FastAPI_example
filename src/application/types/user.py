from datetime import datetime
from typing import TypedDict, NotRequired

class UpdateUserType(TypedDict):
    username: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]
    updated_at: NotRequired[datetime]
