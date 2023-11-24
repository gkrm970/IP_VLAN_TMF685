import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import AppliedCapacityAmount
_ALL_DELETE_ORPHAN = "all, delete-orphan"


class ReservationResource(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    referred_type: Mapped[str] = mapped_column(String(255))
    characteristic: Mapped[list[models.Characteristic]] = relationship(
        back_populates="reservation_resource",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
    )
    href: Mapped[str | None] = mapped_column(String(255))
    resource_id: Mapped[str | None] = mapped_column(String(255))
    # name: Mapped[str | None] = mapped_column(String(255))

    applied_capacity_amount_id: Mapped[str] = mapped_column(
        ForeignKey("applied_capacity_amount.id")
    )
    applied_capacity_amount: Mapped["AppliedCapacityAmount"] = relationship(
        back_populates="reservation_resource"
    )

    @classmethod
    def from_schema(
        cls, referred_type: str, characteristic: list, href: str, resource_id: str
    ) -> "ReservationResource":
        return cls(
            id=str(uuid.uuid4()),
            referred_type=referred_type,
            characteristic=characteristic,
            href=href,
            resource_id=resource_id,
            # name=name
        )
