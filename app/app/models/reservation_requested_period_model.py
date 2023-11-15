import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationRequestedPeriod(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    from_: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="requested_period")

    @classmethod
    def from_schema(cls, schema: schemas.ReservationRequestedPeriod) -> "ReservationRequestedPeriod":
        return cls(
            id=str(uuid.uuid4()),
            from_=schema.from_
        )
