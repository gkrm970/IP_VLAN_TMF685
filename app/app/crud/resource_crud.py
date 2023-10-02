from typing import Any
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Keep abstract base import on top to avoid circular imports
from app.crud.abstract_base import AbstractBaseCRUD  # isort: split
from app import models, schemas


class ResourceCRUD(
    AbstractBaseCRUD[models.Resource, schemas.ResourceCreate, schemas.ResourceUpdate]
):
    async def create(
        self, db: AsyncSession, *, obj_in: schemas.ResourceCreate
    ) -> models.Resource:
        obj_in_data = jsonable_encoder(obj_in)

        db_obj_id = str(uuid4())
        db_obj = models.Resource(
            id=db_obj_id, **obj_in_data
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get(self, db: AsyncSession, id: str) -> models.Resource | None:
        result = await db.execute(select(self.model).filter(self.model.id == id))

        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, limit: int = 100, offset: int = 0
    ) -> tuple[list[models.Resource], int]:
        result = await db.execute(select(self.model).limit(limit).offset(offset))
        total = await db.execute(select(func.count()).select_from(self.model))

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
        db: AsyncSession,
        *,
        db_obj: models.Resource,
        obj_in: schemas.ResourceUpdate | dict[str, Any],
    ) -> models.Resource:
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
    async def delete(db: AsyncSession, *, db_obj: models.Resource) -> models.Resource:
        await db.delete(db_obj)
        await db.commit()

        return db_obj


resource = ResourceCRUD(models.Resource)
