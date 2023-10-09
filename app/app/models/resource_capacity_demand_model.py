import datetime
from datetime import date
from typing import TYPE_CHECKING, Optional

import DateTime
from sqlalchemy import ForeignKey, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ReservationItem


class ResourceCapacityDemand(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    resource_capacity_demand_amount: Mapped[str] = mapped_column(String(255))
    base_type: Mapped[str] = mapped_column(String(255))
    schema_location: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    applicable_time_period: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    valid_for: Mapped[date] = mapped_column(Date, server_default=func.now())
    place: Mapped[str] = mapped_column(String(255))
    pattern: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(255))

    reservation_item_id: Mapped[str] = mapped_column(ForeignKey("reservation_item.id"), unique=True)
    reservation_item: Mapped["ReservationItem"] = relationship(
        back_populates="resource_capacity_demand_ref"
    )

    @classmethod
    def from_schema(cls, schema: schemas.ResourceCapacityDemand | None) -> Optional["ResourceCapacityDemand"]:
        """
        Create a ResourceCapacityDemand object from a schema.

        Args:
            schema (schemas.ResourceCapacityDemand | None): The schema to create the object from.

        Returns:
            Optional[ResourceCapacityDemand]: The created ResourceCapacityDemand object, or None if the schema is None.
        """
        if schema is None:
            return None

        return cls(**schema.model_dump())
