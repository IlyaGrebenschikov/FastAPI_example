from datetime import timedelta

from backend.src.common.dto.user import UserSchema, UserResponseSchema, UpdateUserQuerySchema, UserInDBSchema
from backend.src.services.security.bcrypt_hasher import BcryptHasher
from backend.src.cache.core.client import RedisClient
from backend.src.database.repositories.user import UserRepository
from backend.src.common.converters.database import from_model_to_dto
from backend.src.common.converters.user import convert_sending, convert_receiving, none_filter
from backend.src.common.converters.cache import from_dict_to_dto
from backend.src.common.exceptions import NotFoundException


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def create(self, data: UserSchema, hasher: BcryptHasher) -> UserResponseSchema:
        data.password = hasher.hash_password(data.password)

        return from_model_to_dto(await self._repository.create(**data.model_dump()), UserResponseSchema)

    async def update(
            self,
            data: UpdateUserQuerySchema,
            user_id: int,
            user_ttl: int,
            hasher: BcryptHasher,
            cache: RedisClient
    ) -> UserResponseSchema:
        filtered_data = none_filter(data)

        if filtered_data.get('password'):
            filtered_data['password'] = hasher.hash_password(filtered_data['password'])

        result = await self._repository.update(user_id, **filtered_data)

        await cache.set_dict(
            user_id,
            convert_sending(from_model_to_dto(result, UserInDBSchema).model_dump())
        )
        await cache.set_expire(user_id, timedelta(minutes=user_ttl))

        return from_model_to_dto(result, UserResponseSchema)

    async def get(self, user_id: int, user_ttl: int, cache: RedisClient) -> UserInDBSchema:
        cached_data = await cache.get_dict_all(user_id)

        if cached_data:
            return from_dict_to_dto(convert_receiving(cached_data), UserInDBSchema)

        result = await self._repository.get_one(user_id=user_id)

        if not result:
            raise NotFoundException('User not found')

        converted_result = from_model_to_dto(result, UserInDBSchema)

        await cache.set_dict(user_id, convert_sending(converted_result.model_dump()))
        await cache.set_expire(user_id, timedelta(minutes=user_ttl))

        return converted_result

    async def delete(self, user_id: int, cache: RedisClient) -> UserResponseSchema:
        result = await self._repository.delete(user_id)

        await cache.delete(user_id)

        return from_model_to_dto(result, UserResponseSchema)
