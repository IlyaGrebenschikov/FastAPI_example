from typing import Callable

from backend.src.common.types import DependencyType


def singleton(value: DependencyType) -> Callable[[], DependencyType]:
    def singleton_factory() -> DependencyType:
        return value

    return singleton_factory
