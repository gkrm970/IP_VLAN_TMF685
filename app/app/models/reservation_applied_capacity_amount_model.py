import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas, models
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationItem

_ALL_DELETE_ORPHAN = "all, delete-orphan"


class AppliedCapacityAmount(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    applied_capacity_amount: Mapped[str] = mapped_column(String(255))
    reservation_resource: Mapped[list[models.ReservationResource]] = relationship(
        back_populates="applied_capacity_amount", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )

    reservation_item_id: Mapped[str] = mapped_column(ForeignKey("reservation_item.id"))
    reservation_item: Mapped["ReservationItem"] = relationship(
        back_populates="applied_capacity_amount"
    )

    @classmethod
    def from_schema(cls, schema: schemas.AppliedCapacityAmount) -> "AppliedCapacityAmount":
        reservation_resource = [
            models.ReservationResource.from_schema(reservation_resource)
            for reservation_resource in schema.reservation_resource
        ]

        return cls(
            # id=str(uuid.uuid4()),
            applied_capacity_amount=schema.applied_capacity_amount,
            reservation_resource=reservation_resource
        )
