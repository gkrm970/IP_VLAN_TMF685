from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import log, models, schemas
from app.core.exceptions import ConflictError, NotFoundError


class ReservationCRUD:
    @staticmethod
    async def get_by_resource_pool_id(
        db: AsyncSession, id: str
    ) -> models.ReservationResourcePool | None:
        result = await db.execute(
            select(models.ReservationResourcePool).filter(
                models.ReservationResourcePool.id == id
            )
        )
        return result.scalars().first()

    @staticmethod
    async def validate_resource_pool_id(db: AsyncSession, resource_pool_id: str):
        existing_resource_pool_id = await ReservationCRUD.get_by_resource_pool_id(
            db, resource_pool_id
        )

        if existing_resource_pool_id is not None:
            raise ConflictError(
                f"resourcePool with id {resource_pool_id} already exists"
            )

    @staticmethod
    async def create(
        db: AsyncSession, obj_in: schemas.ReservationCreate
    ) -> models.Reservation:
        # resource_pool_id = obj_in.reservation_item[
        #     0
        # ].reservation_resource_capacity.resource_pool.pool_id
        # log.info(f"{resource_pool_id=}")

        # result = await db.execute(
        #     select(models.ResourcePool).filter(
        #         models.ResourcePool.id == resource_pool_id
        #     )
        # )
        # existing_resource_pool_id_11 = result.scalars().first()
        #
        # log.info(f"{existing_resource_pool_id_11=}")
        # if existing_resource_pool_id_11 is None:
        #     raise NotFoundError(f"resourcePool with id {resource_pool_id} not found")
        # await ReservationCRUD.validate_resource_pool_id(db, resource_pool_id)
        reservation_state = "completed"
        current_datetime = datetime.utcnow()
        # valid_for_dict = {"startDate": current_datetime}

        db_obj = models.Reservation.from_schema(obj_in, reservation_state=reservation_state, valid_for=current_datetime)
        print("db_obj", db_obj)

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
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[models.Reservation], int]:
        result = await db.execute(
            select(models.Reservation).limit(limit).offset(offset)
        )
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
