from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from user_service.src.common.dto.user import UserResponseSchema, UserSchema
from user_service.src.api.v1.handlers.user.create import CreateUserHandler
from user_service.src.api.v1.handlers.user.get_current import GetCurrentUserHandler
from user_service.src.api.v1.handlers.user.update import UpdateUserHandler
from user_service.src.common.exceptions import ConflictException, NotFoundException, UnAuthorizedException
from user_service.src.common.dto.docs import ConflictError, NotFoundError, UnauthorizedError


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

    except ConflictException as conflict_error:
        raise HTTPException(status.HTTP_409_CONFLICT, conflict_error.get_dict())


@user_router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
    response_description='User resource',
    description='Retrieves a User resource',
    summary='Retrieves a User resource',
    responses={
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {'model': UnauthorizedError}
    },
)
async def get_user(
        handler: Annotated[GetCurrentUserHandler, Depends(GetCurrentUserHandler)]
) -> UserResponseSchema:
    try:
        return await handler.execute()

    except NotFoundException as not_found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, not_found.get_dict())

    except UnAuthorizedException as un_authorized_error:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, un_authorized_error.get_dict())


@user_router.patch(
    '',
    response_model=UserResponseSchema,
    response_description='User resource updated',
    description='Updates user data',
    summary='Updates user data',
    responses={
        status.HTTP_409_CONFLICT: {'model': ConflictError},
        status.HTTP_404_NOT_FOUND: {'model': NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {'model': UnauthorizedError}
    }
)
async def update_user(
        body: UserSchema,
        current_user_handler: Annotated[GetCurrentUserHandler, Depends(GetCurrentUserHandler)],
        update_user_handler: Annotated[UpdateUserHandler, Depends(UpdateUserHandler)]
):
    try:
        current_user = await current_user_handler.execute()
        result = await update_user_handler.execute(current_user, body)
        return result

    except ConflictException as conflict_error:
        raise HTTPException(status.HTTP_409_CONFLICT, conflict_error.get_dict())

    except NotFoundException as not_found:
        raise HTTPException(status.HTTP_404_NOT_FOUND, not_found.get_dict())

    except UnAuthorizedException as un_authorized_error:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, un_authorized_error.get_dict())
