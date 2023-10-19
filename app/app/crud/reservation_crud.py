from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


class ReservationCRUD:
    @staticmethod
    async def create(
        db: AsyncSession, *, obj_in: schemas.ReservationCreate
    ) -> models.Reservation:
        db_obj = models.Reservation.from_schema(obj_in)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def get(db: AsyncSession, id: str) -> models.Reservation | None:
        result = await db.execute(
            select(models.Reservation).filter(models.Reservation.id == id)
        )

        return result.scalars().first()

    @staticmethod
    async def get_multi(
        db: AsyncSession,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[models.Reservation], int]:
        result = await db.execute(select(models.Reservation).limit(limit).offset(offset))
        total = await db.execute(select(func.count()).select_from(models.Reservation))

        return list(result.scalars().all()), total.scalar() or 0

    @staticmethod
    async def update(
            db: AsyncSession,
            db_obj: models.Reservation,
            update_schema: schemas.ReservationUpdate,
    ) -> models.Reservation:
        db_obj.update(update_schema)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: models.Reservation) -> None:
        await db.delete(db_obj)
        await db.commit()


reservation = ReservationCRUD()
