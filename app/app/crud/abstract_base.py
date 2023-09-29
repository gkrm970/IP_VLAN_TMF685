from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

# SQLAlchemy Model
ModelType = TypeVar("ModelType", bound=Base)

# Pydantic Schema Models
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AbstractBaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @abstractmethod
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    async def get(self, db: AsyncSession, id: str) -> ModelType | None:
        pass

    @abstractmethod
    async def get_multi(
        self, db: AsyncSession, *, limit: int = 100, offset: int = 0
    ) -> tuple[list[ModelType], int]:
        pass

    @staticmethod
    @abstractmethod
    async def update(
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        pass

    @staticmethod
    @abstractmethod
    async def delete(db: AsyncSession, *, db_obj: ModelType) -> ModelType:
        pass
