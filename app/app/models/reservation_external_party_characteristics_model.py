import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationResourceCapacity


class ExternalPartyCharacteristics(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    ipam_description: Mapped[str | None] = mapped_column(String(255))
    ipam_details: Mapped[str | None] = mapped_column(String(255))

    reservation_resource_capacity_id: Mapped[str] = mapped_column(
        ForeignKey("reservation_resource_capacity.id")
    )
    reservation_resource_capacity: Mapped["ReservationResourceCapacity"] = relationship(
        back_populates="external_party_characteristics"
    )

    @classmethod
    def from_schema(
        cls, schema: schemas.ExternalPartyCharacteristics
    ) -> "ExternalPartyCharacteristics":
        return cls(
            id=str(uuid.uuid4()),
            ipam_description=schema.ipam_description,
            ipam_details=schema.ipam_details,
        )
