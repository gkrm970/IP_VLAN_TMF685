from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationItem(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    quantity: Mapped[int | None] = mapped_column(String(255))
    sub_reservation_state: Mapped[str | None] = mapped_column(String(255))
    applied_capacity_amount: Mapped[str | None] = mapped_column(String(255))
    base_type: Mapped[str | None] = mapped_column(String(255))
    schema_location: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))

    # # 1..1 relationship with Reservation table and RelatedPartyRef table (RelatedPartyRef table is child)
    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"), unique=True)
    reservation: Mapped["Reservation"] = relationship(
        back_populates="reservation_item_ref"
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationItem) -> "ReservationItem":
        return cls(**schema.model_dump())
