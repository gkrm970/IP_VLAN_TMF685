import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationResourceCapacity


class ReservationPlace(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))

    reservation_resource_capacity_id: Mapped[str] = mapped_column(
        ForeignKey("reservation_resource_capacity.id")
    )
    reservation_resource_capacity: Mapped["ReservationResourceCapacity"] = relationship(
        back_populates="reservation_place"
    )

    @classmethod
    def from_schema(cls, schema: schemas.Place) -> "ReservationPlace":
        return cls(
            id=str(uuid.uuid4()),
            name=schema.name,
            type=schema.type
        )
