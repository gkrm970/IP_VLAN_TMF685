from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base


if TYPE_CHECKING:
    from app.models import Reservation


class RelatedPartyRef(Base):
    __tablename__ = 'related_party_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    referred_type: Mapped[str | None] = mapped_column(String(255))
    href: Mapped[str | None] = mapped_column(String(255))
    name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str | None] = mapped_column(String(255))

    # # 1..1 relationship with Reservation table and RelatedPartyRef table (RelatedPartyRef table is child)
    reservation_id: Mapped[str] = mapped_column(String), ForeignKey("reservation.id")
    reservation: Mapped["Reservation"] = relationship(back_populates="related_party_ref")  # 1..1

    @classmethod
    def from_schema(cls, schema: schemas.RelatedPartyRef) -> "RelatedPartyRef":
        return cls(**schema.model_dump())

