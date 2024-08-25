from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from user_service.src.common.dto.user import UserResponseSchema, UserSchema
from user_service.src.api.v1.handlers.user.create import CreateUserHandler
from user_service.src.common.exceptions import UserAlreadyExistsException
from user_service.src.common.dto.docs import ConflictError


user_router = APIRouter(tags=['user'])


@user_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseSchema,
    response_description='User resource created',
    description='Creates a User resource',
    summary='Creates a User resource',
    responses={
        status.HTTP_409_CONFLICT: {'model': ConflictError},
    },
)
async def create_user(
        body: UserSchema,
        handler: Annotated[CreateUserHandler, Depends(CreateUserHandler)],
) -> UserResponseSchema:
    try:
        return await handler.execute(body)

    except UserAlreadyExistsException as exists_error:
        raise HTTPException(status.HTTP_409_CONFLICT, exists_error.get_dict())
