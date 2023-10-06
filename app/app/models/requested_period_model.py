from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class RequestedPeriod(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    base_type: Mapped[str] = mapped_column(String(255))
    schema_location: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    days_of_week: Mapped[str] = mapped_column(String(255))
    from_to_date_time: Mapped[str] = mapped_column(String(255))
    range_interval: Mapped[str] = mapped_column(String(255))
    valid_for: Mapped[date] = mapped_column(Date, server_default=func.now())

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"), unique=True)
    reservation: Mapped["Reservation"] = relationship(
        back_populates="requested_period_ref")

    @classmethod
    def from_schema(cls, schema: schemas.RequestedPeriod | None) -> Optional["RequestedPeriod"]:
        if schema is None:
            return None

        return cls(**schema.model_dump())
