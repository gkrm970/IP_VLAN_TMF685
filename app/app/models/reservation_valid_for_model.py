import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import Reservation


class ValidFor(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    start_date: Mapped[str] = mapped_column(String(255))

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="valid_for")

    @classmethod
    def from_schema(cls, schema: schemas.ReservationValidFor) -> "ValidFor":
        return cls(
            # id=str(uuid.uuid4()),
            start_date=schema.start_date
        )
