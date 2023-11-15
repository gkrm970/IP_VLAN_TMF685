import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import BaseDbModel

_ALL_DELETE_ORPHAN = "all, delete-orphan"

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationItem(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer)

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="reservation_item")
    reservation_resource_capacity: Mapped[
        models.ReservationResourceCapacity
    ] = relationship(
        back_populates="reservation_item",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
        uselist=False,
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationItem) -> "ReservationItem":
        reservation_item = str(uuid.uuid4())
        reservation_resource_capacity = models.ReservationResourceCapacity.from_schema(
            schema.reservation_resource_capacity
        )
        return cls(
            id=reservation_item,
            quantity=schema.quantity,
            reservation_resource_capacity=reservation_resource_capacity,
        )
