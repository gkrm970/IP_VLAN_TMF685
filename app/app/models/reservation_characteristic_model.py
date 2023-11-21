import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationResource


class Characteristic(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    ipv4_subnet: Mapped[str] = mapped_column(String(255))

    reservation_resource_id: Mapped[str] = mapped_column(ForeignKey("reservation_resource.id"))
    reservation_resource: Mapped["ReservationResource"] = relationship(back_populates="characteristic")

    @classmethod
    def from_schema(cls, schema: schemas.ReservationCharacteristic) -> "Characteristic":
        return cls(
            # id=str(uuid.uuid4()),
            ipv4_subnet=schema.ipv4_subnet,
        )
