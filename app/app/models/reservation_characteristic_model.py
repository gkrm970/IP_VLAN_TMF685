import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ReservationResource


class Characteristic(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    ipv4_subnet: Mapped[str] = mapped_column(String(255))
    ipv6_subnet: Mapped[str] = mapped_column(String(255))
    vlan_8021q: Mapped[str] = mapped_column(String(255))

    reservation_resource_id: Mapped[str] = mapped_column(
        ForeignKey("reservation_resource.id")
    )
    reservation_resource: Mapped["ReservationResource"] = relationship(
        back_populates="characteristic"
    )

    @classmethod
    def from_schema(
        cls, ipv4_subnet: str, ipv6_subnet: str, vlan_8021q: str
    ) -> "Characteristic":
        return cls(
            id=str(uuid.uuid4()),
            ipv4_subnet=ipv4_subnet,
            ipv6_subnet=ipv6_subnet,
            vlan_8021q=vlan_8021q,
        )
