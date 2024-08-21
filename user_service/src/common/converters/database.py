from typing import Type

from user_service.src.common.types import ModelType, DTOType


def from_model_to_dto(model: ModelType, dto: Type[DTOType]) -> DTOType:
    return dto(**model.as_dict())
