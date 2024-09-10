from typing import Optional

from backend.src.common.types import DTOType


def none_filter(data: Optional[DTOType | dict]) -> dict:
    return {k: v for k, v in data.model_dump().items() if v}

