import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas, models
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ResourcePoolManagement


class Capacity(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, default=True, autoincrement=True
                                    )
    capacity_amount: Mapped[int] = mapped_column(Integer)
    capacity_amount_from: Mapped[str] = mapped_column(String(255))
    capacity_amount_to: Mapped[str] = mapped_column(String(255))

    resource_pool_id: Mapped[str] = mapped_column(ForeignKey("resource_pool_management.id"))
    resource_pool: Mapped["ResourcePoolManagement"] = relationship(back_populates="resource_capacity", uselist=False)

    # resource_id: Mapped[str] = mapped_column(ForeignKey("resource.id"))
    # resource: Mapped["Resource"] = relationship(back_populates="related_parties")

    place: Mapped[list[models.ResourcePlace]] = relationship(
        back_populates="capacity", lazy="selectin", cascade="all, delete-orphan"
    )
    related_party: Mapped[list[models.ResourceRelatedParty]] = relationship(
        back_populates="capacity", lazy="selectin", cascade="all, delete-orphan"
    )

    # place_id: Mapped[str] = mapped_column(ForeignKey("resource_place.id"), unique=True)
    # place: Mapped[models.ResourcePlace] = relationship(
    #     back_populates="capacity")
    #
    # related_party_id: Mapped[str] = mapped_column(ForeignKey("resource_related_party.id"), unique=True)
    # related_party: Mapped[models.ResourceRelatedParty] = relationship(
    #     back_populates="capacity")

    @classmethod
    def from_schema(cls, schema: schemas.ResourceCapacity | None) -> Optional["Capacity"]:
        # capacity_id = str(uuid.uuid4())
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
