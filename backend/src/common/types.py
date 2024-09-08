from typing import TypeVar

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


SessionFactory = TypeVar("SessionFactory")
ModelType = TypeVar("ModelType", bound='Base')
GatewayType = TypeVar("GatewayType", bound="BaseGateway")
RepositoryType = TypeVar("RepositoryType", bound="Repository")
DTOType = TypeVar("DTOType", bound="DTO")
SessionFactoryType = async_sessionmaker[AsyncSession]
DependencyType = TypeVar("DependencyType")
