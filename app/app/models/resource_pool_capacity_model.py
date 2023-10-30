import uuid
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas, models
from app.db.base import BaseDbModel

if TYPE_CHECKING:
    from app.models import ResourcePoolManagement


class Capacity(BaseDbModel):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    capacity_amount: Mapped[int] = mapped_column(Integer)
    capacity_amount_from: Mapped[str] = mapped_column(String(255))
    capacity_amount_to: Mapped[str] = mapped_column(String(255))

    resource_pool_id: Mapped[str] = mapped_column(
        ForeignKey("resource_pool_management.id")
    )
    resource_pool_management: Mapped["ResourcePoolManagement"] = relationship(
        back_populates="resource_capacity"
    )

    place: Mapped[list[models.ResourcePlace]] = relationship(
        back_populates="capacity", lazy="selectin", cascade="all, delete-orphan"
    )
    related_party: Mapped[models.ResourceRelatedParty] = relationship(
        back_populates="capacity",
        lazy="selectin",
        cascade="all, delete-orphan",
        uselist=False,
    )

    @classmethod
    def from_schema(cls, schema: schemas.ResourceCapacity) -> "Capacity":
        print(f"schema:{schema}")
        # capacity_id = str(uuid.uuid4())
        related_party = models.ResourceRelatedParty.from_schema(schema.related_party)

        place = [models.ResourcePlace.from_schema(places) for places in schema.place]

        dict_data = {
            # "id":capacity_id,
            "capacity_amount": schema.capacity_amount,
            "capacity_amount_from": schema.capacity_amount_from,
            "capacity_amount_to": schema.capacity_amount_to,
            "related_party": related_party,
            "place": place,
        }

        print(f"{dict_data=}")
        return cls(**dict_data)
