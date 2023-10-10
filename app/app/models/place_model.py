from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ResourcePool


class ResourceRef(Base):
    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, index=True, default=True
    )

    name: Mapped[str] = mapped_column(String(255))
    object_id: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    # ResourcePool and ResourceCollection are one-to-one relationship(ResourceCollection  is child of ResourcePool)
    resource_pool_id: Mapped[str] = mapped_column(
        ForeignKey("resource_pool.id"), unique=True
    )
    resource_ref: Mapped["ResourcePool"] = relationship(back_populates="resource_ref")

    @classmethod
    def from_schema(cls, schema: schemas.ResourceRef | None) -> Optional["ResourceRef"]:
        """
        Create a ResourceCollection object from a schema.

        Args:
            schema (schemas.ResourceCollection | None): The schema to create the object from.

        Returns:
            Optional[ResourceCollection]: The created ResourceCollection object, or None if the schema is None.
        """
        if schema is None:
            return None

        return cls(**schema.model_dump())
