import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationRelatedParty(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str | None] = mapped_column(String(255))

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="related_parties")

    @classmethod
    def from_schema(
        cls, schema: schemas.RelatedParty | None
    ) -> Optional["ReservationRelatedParty"]:
        # schema.id = schema.id or str(uuid.uuid4())
        if schema is None:
            return None
        return cls(id=str(uuid.uuid4()), name=schema.name, role=schema.role)
