from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.crud.abstract_base import AbstractBaseCRUD


class ResourcePoolCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, *, obj_in: schemas.ResourcePoolManagementCreate
    ) -> models.ResourcePoolManagement:
        db_obj = models.ResourcePoolManagement.from_schema(obj_in)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def get(db: AsyncSession, *, id: str) -> models.ResourcePoolManagement | None:
        result = await db.execute(
            select(models.ResourcePoolManagement).filter(models.ResourcePoolManagement.id == id)
        )

        return result.scalars().first()

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[models.ResourcePoolManagement], int]:
        result = await db.execute(select(models.ResourcePoolManagement).limit(limit).offset(offset))
        total = await db.execute(select(func.count()).select_from(models.ResourcePoolManagement))

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
        db: AsyncSession,
        *,
        db_obj: models.ResourcePoolManagement,
        obj_in: schemas.ResourcePoolManagementUpdate | dict[str, Any],
    ) -> models.ResourcePoolManagement:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, *, db_obj: models.ResourcePoolManagement) -> models.ResourcePoolManagement:
        await db.delete(db_obj)
        await db.commit()

        return db_obj


resource_pool = ResourcePoolCRUD()
