from .base import BaseResponseDTO


class DeleteUserResponseDTO(BaseResponseDTO):
    message: str = "deleted"
