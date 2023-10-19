import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationItem

_ALL_DELETE_ORPHAN = "all, delete-orphan"


class ReservationResourceCapacity(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(255))
    capacity_demand_amount: Mapped[str] = mapped_column(String(255))

    reservation_applicable_time_period: Mapped[models.ReservationApplicableTimePeriod] = relationship(
        back_populates="reservation_resource_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )
    reservation_place: Mapped[list[models.ReservationPlace]] = relationship(
        back_populates="reservation_resource_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )
    resource_pool: Mapped[models.ReservationResourcePool] = relationship(
        back_populates="reservation_resource_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )

    reservation_item_id: Mapped[str] = mapped_column(ForeignKey("reservation_item.id"))
    reservation_item: Mapped["ReservationItem"] = relationship(back_populates="reservation_resource_capacity")

    @classmethod
    def from_schema(cls, schema: schemas.ReservationResourceCapacity) -> "ReservationResourceCapacity":
        reservation_applicable_time_period = models.ReservationApplicableTimePeriod.from_schema(schema.reservation_applicable_time_period)
        reservation_place = [
            models.ReservationPlace.from_schema(reservation_place)
            for reservation_place in schema.reservation_place
        ]
        resource_pool = models.ReservationResourcePool.from_schema(schema.resource_pool)

        return cls(
            id=schema.id or str(uuid.uuid4()),
            type=schema.type,
            capacity_demand_amount=schema.capacity_demand_amount,
            reservation_applicable_time_period=reservation_applicable_time_period,
            reservation_place=reservation_place,
            resource_pool=resource_pool
        )


