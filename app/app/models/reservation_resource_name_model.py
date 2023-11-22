import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationItem


class ReservationResourceName(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    reservation_item_id: Mapped[str] = mapped_column(ForeignKey("reservation_item.id"))
    reservation_item: Mapped["ReservationItem"] = relationship(
        back_populates="resource_name"
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationResourceName) -> "ReservationResourceName":
        return cls(
            id=str(uuid.uuid4()),
            name=schema.name,
        )
