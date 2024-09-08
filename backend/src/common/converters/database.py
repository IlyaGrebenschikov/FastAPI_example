from typing import Type

from backend.src.common.types import ModelType, DTOType


def from_model_to_dto(model: ModelType, dto: Type[DTOType]) -> DTOType:
    return dto(**model.as_dict())
