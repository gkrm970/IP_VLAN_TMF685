from typing import Any
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Keep abstract base import on top to avoid circular imports
from app.crud.abstract_base import AbstractBaseCRUD  # isort: split
from app import models, schemas, log


class ReservationCRUD(
    AbstractBaseCRUD[models.Reservation, schemas.ReservationCreate, schemas.ReservationUpdate]
):

    async def create(
        self, db: AsyncSession, *, obj_in: schemas.ReservationCreate
    ) -> models.Reservation:
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = models.Reservation.from_schema(obj_in)

        # db_obj_id = str(uuid4())
        # db_obj = models.Reservation(
        #     id=db_obj_id, **obj_in_data
        # )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get(self, db: AsyncSession, id: str) -> models.Reservation | None:
        result = await db.execute(select(self.model).filter(self.model.id == id))

        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, limit: int = 100, offset: int = 0
    ) -> tuple[list[models.Reservation], int]:
        result = await db.execute(select(self.model).limit(limit).offset(offset))
        total = await db.execute(select(func.count()).select_from(self.model))

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
        db: AsyncSession,
        *,
        db_obj: models.Reservation,
        obj_in: schemas.ReservationUpdate | dict[str, Any],
    ) -> models.Reservation:
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
    async def delete(db: AsyncSession, *, db_obj: models.Reservation) -> models.Reservation:
        await db.delete(db_obj)
        await db.commit()

        return db_obj


reservation = ReservationCRUD(models.Reservation)
