from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


class ResourcePoolCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, obj_in: schemas.ResourcePoolManagementCreate
    ) -> models.ResourcePoolManagement:
        db_obj = models.ResourcePoolManagement.from_schema(obj_in)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def get(db: AsyncSession, id: str) -> models.ResourcePoolManagement | None:
        result = await db.execute(
            select(models.ResourcePoolManagement).filter(
                models.ResourcePoolManagement.id == id
            )
        )

        return result.scalars().first()

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[models.ResourcePoolManagement], int]:
        result = await db.execute(
            select(models.ResourcePoolManagement).limit(limit).offset(offset)
        )
        total = await db.execute(
            select(func.count()).select_from(models.ResourcePoolManagement)
        )

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
        db: AsyncSession,
        db_obj: models.ResourcePoolManagement,
        update_schema: schemas.ResourcePoolManagementUpdate,
    ) -> models.ResourcePoolManagement:
        db_obj.update(update_schema)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: models.ResourcePoolManagement) -> None:
        await db.delete(db_obj)
        await db.commit()


resource_pool = ResourcePoolCRUD()
