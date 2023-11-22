import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationResourceCapacity


class ReservationApplicableTimePeriod(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    from_: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))

    reservation_resource_capacity_id: Mapped[str] = mapped_column(
        ForeignKey("reservation_resource_capacity.id")
    )
    reservation_resource_capacity: Mapped["ReservationResourceCapacity"] = relationship(
        back_populates="reservation_applicable_time_period"
    )

    @classmethod
    def from_schema(
        cls, schema: schemas.ReservationApplicableTimePeriod
    ) -> "ReservationApplicableTimePeriod":
        return cls(id=str(uuid.uuid4()), from_=schema.from_)
