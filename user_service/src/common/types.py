from typing import TypeVar


SessionFactory = TypeVar("SessionFactory")
ModelType = TypeVar("ModelType", bound='Base')
