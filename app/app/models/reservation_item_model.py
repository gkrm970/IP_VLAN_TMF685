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
    applied_capacity_amount: Mapped[models.AppliedCapacityAmount] = relationship(
        back_populates="reservation_item",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
        uselist=False,
    )
    quantity: Mapped[int] = mapped_column(Integer)
    resource_name: Mapped[list[models.ReservationResourceName]] = relationship(
        back_populates="reservation_item", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )

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
    sub_reservation_state: Mapped[str | None] = mapped_column(String(255))

    @classmethod
    def from_schema(
        cls,
        schema: schemas.ReservationItem,
        sub_reservation_state: str,
        applied_capacity_amount: schemas.AppliedCapacityAmount,
    ) -> "ReservationItem":
        reservation_item = str(uuid.uuid4())

        # applied_capacity_amount_instance = (models.AppliedCapacityAmount. from_schema(applied_capacity_amount,
        # reservation_resource=reservation_resource))

        reservation_resource_capacity = models.ReservationResourceCapacity.from_schema(
            schema.reservation_resource_capacity
        )
        resource_name = [
            models.ReservationResourceName.from_schema(resource_name)
            for resource_name in schema.resource_name
        ]

        return cls(
            id=reservation_item,
            applied_capacity_amount=applied_capacity_amount,
            quantity=schema.quantity,
            resource_name=resource_name,
            reservation_resource_capacity=reservation_resource_capacity,
            sub_reservation_state=sub_reservation_state,
        )
