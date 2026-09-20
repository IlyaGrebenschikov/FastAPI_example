from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    pass


class BaseResponseDTO(BaseDTO):
    model_config = ConfigDict(from_attributes=True)
