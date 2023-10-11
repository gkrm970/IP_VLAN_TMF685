from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.crud.abstract_base import AbstractBaseCRUD


class ResourceCRUD(AbstractBaseCRUD
                   [models.ResourceSpecification, schemas.ResourceSpecificationCreate, schemas.ResourceSpecificationUpdate]):
    async def create(self, db: AsyncSession, *,
                     obj_in: schemas.ResourceSpecificationCreate) -> models.ResourceSpecification:
        db_obj = models.ResourceSpecification.from_schema(obj_in)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get(self, db: AsyncSession, id: str) -> models.ResourceSpecification | None:
        result = await db.execute(select(self.model).filter(self.model.id == id))

        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, limit: int = 100, offset: int = 0) -> tuple[
        list[models.ResourceSpecification], int]:
        result = await db.execute(select(self.model).limit(limit).offset(offset))
        total = await db.execute(select(func.count()).select_from(self.model))

        return list(result.scalars().all()), total.scalar() or 0

    async def update(self,
                     id: str,
                     db: AsyncSession,
                     *,
                     db_obj: models.ResourceSpecification,
                     obj_in: schemas.ResourceSpecificationUpdate | dict[str, Any],
                     ) -> models.ResourceSpecification:
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


resource_pool = ResourceCRUD(models.ResourceSpecification)
