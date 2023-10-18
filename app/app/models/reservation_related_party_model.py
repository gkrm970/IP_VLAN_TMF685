import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationRelatedParty(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str | None] = mapped_column(String(255))

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="related_parties")

    @classmethod
    def from_schema(cls, schema: schemas.RelatedParty) -> "ReservationRelatedParty":
        schema.id = schema.id or str(uuid.uuid4())
        return cls(**schema.model_dump())
