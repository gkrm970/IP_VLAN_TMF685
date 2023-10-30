import random
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas

_existing_reservation_id = str(uuid.uuid4())

EXISTING_RESERVATION = models.Reservation(
    reservation_state="test_name",
    id=_existing_reservation_id,
    href=f"resourcePool/{_existing_reservation_id}",
)


async def get_multi(
    _db: AsyncSession,
    _limit: int = 100,
    _offset: int = 0,
) -> tuple[list[models.Reservation], int]:
    reservations = []
    number_of_reservation = random.randint(1, 10)

    for _ in range(number_of_reservation):
        db_obj_id = str(uuid.uuid4())

        reservations.append(
            models.Reservation(
                type="test_type",
                reservation_state="test_name",
                id=db_obj_id,
                href=f"reservation/{db_obj_id}",
            )
        )

    return reservations, number_of_reservation


async def create(
    _db: AsyncSession, _obj_in: schemas.ReservationCreate
) -> models.Reservation:
    db_obj_id = str(uuid.uuid4())

    return models.Reservation(
        reservation_state="test_name", id=db_obj_id, href=f"reservation/{db_obj_id}"
    )


async def get(_db: AsyncSession, id: str) -> models.Reservation | None:
    if id == EXISTING_RESERVATION.id:
        return EXISTING_RESERVATION

    return None


async def delete(_db: AsyncSession, _db_obj: models.Reservation) -> None:
    return None


async def update(_db: AsyncSession, _db_obj: models.Reservation) -> None:
    return None
