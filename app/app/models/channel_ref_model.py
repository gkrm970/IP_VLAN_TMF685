from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ChannelRef(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referred_type: Mapped[str] = mapped_column(String(255))

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"), unique=True)
    reservation: Mapped["Reservation"] = relationship(
        back_populates="channel_ref"
    )

    @classmethod
    def from_schema(cls, schema: schemas.ChannelRef | None) -> Optional["ChannelRef"]:
        if schema is None:
            return None

        return cls(**schema.model_dump())
