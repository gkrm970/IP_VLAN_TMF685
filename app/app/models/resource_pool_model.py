import datetime
from datetime import date
from typing import TYPE_CHECKING, Optional

import DateTime
from sqlalchemy import ForeignKey, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ResourceCapacityDemand


class ResourcePool(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    related_party: Mapped[str] = mapped_column(String(255))
    resource_collection: Mapped[str] = mapped_column(String(255))
    base_type: Mapped[str] = mapped_column(String(255))
    schema_location: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))

    # Resource pool and ResourceCapacityDemand are one-to-one relation (ResourcePool is child of ResourceCapacityDemand)
    resource_pool_id: Mapped[str] = mapped_column(ForeignKey("resource_capacity_demand.id"), unique=True)
    resource_capacity_demand_ref: Mapped["ResourceCapacityDemand"] = relationship(
        back_populates="resource_pool_ref")

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePool | None) -> Optional["ResourcePool"]:
        """
        Create a ResourcePool object from a schema.

        Args:
            schema (schemas.ResourcePool | None): The schema to create the object from.

        Returns:
            Optional[ResourcePool]: The created ResourcePool object, or None if the schema is None.
        """
        if schema is None:
            return None

        return cls(**schema.model_dump())


