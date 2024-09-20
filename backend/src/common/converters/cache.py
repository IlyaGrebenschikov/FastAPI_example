from typing import Type

from backend.src.common.types import DTOType


def from_dict_to_dto(data: dict, dto: Type[DTOType]) -> DTOType:
    return dto(**data)
