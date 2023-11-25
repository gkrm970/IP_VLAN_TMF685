from app import models, schemas, settings
from sqlalchemy import func, select
from urllib.parse import urljoin
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers import resource_catalog_provider
from app.core.exceptions import BadRequestError
from fastapi import status


class ResourcePoolCRUD:
    def __init__(self):
        self.base_api_url = urljoin(str(settings.RC_BASE_URL), settings.RC_API_PREFIX)

    async def create(
        self, db: AsyncSession, obj_in: schemas.ResourcePoolCreate
    ) -> models.ResourcePool:
        db_obj = models.ResourcePool.from_schema(obj_in)
        resource_specification_id = (
            obj_in.capacity[0].resource_specification[0].resource_specification_id
        )
        resource_specification_url = (
            f"{self.base_api_url}/resourceSpecification/{resource_specification_id}"
        )
        resource_specification_res = await resource_catalog_provider.send_request(
            "GET", resource_specification_url
        )
        if resource_specification_res.status_code == status.HTTP_200_OK:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        else:
            raise BadRequestError(
                f"Resource Specification not found this id {resource_specification_id}"
            )

    @staticmethod
    async def get(db: AsyncSession, id: str) -> models.ResourcePool | None:
        result = await db.execute(
            select(models.ResourcePool).filter(models.ResourcePool.id == id)
        )

        return result.scalars().first()

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[models.ResourcePool], int]:
        result = await db.execute(
            select(models.ResourcePool).limit(limit).offset(offset)
        )
        total = await db.execute(select(func.count()).select_from(models.ResourcePool))

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
        db: AsyncSession,
        db_obj: models.ResourcePool,
        update_schema: schemas.ResourcePoolUpdate,
    ) -> models.ResourcePool:
        db_obj.update(update_schema)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: models.ResourcePool) -> None:
        await db.delete(db_obj)
        await db.commit()


resource_pool = ResourcePoolCRUD()
