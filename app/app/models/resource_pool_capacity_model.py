import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from app import models, schemas
from app.db.base import BaseDbModel

# Cascade rule for SQLAlchemy relationship. The all symbol is a synonym for save-update,
# merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan
# indicates that the child object should follow along with its parent in all cases, and
# be deleted once it is no longer associated with that parent
_ALL_DELETE_ORPHAN = "all, delete-orphan"
if TYPE_CHECKING:
    from app.models import ResourcePool


class ResourcePoolCapacity(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)

    applicable_time_period: Mapped[models.ResourcePoolApplicableTimePeriod] = relationship(
        back_populates="resource_pool_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )
    capacity_amount: Mapped[str | None] = mapped_column(String(255))
    capacity_amount_from: Mapped[str | None] = mapped_column(String(255))
    capacity_amount_remaining: Mapped[str | None] = mapped_column(String(255))
    capacity_amount_to: Mapped[str | None] = mapped_column(String(255))
    range_interval: Mapped[str | None] = mapped_column(String(255))
    related_party: Mapped[models.ResourcePoolRelatedParty] = relationship(
        back_populates="resource_pool_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )
    place: Mapped[list[models.ResourcePoolPlace]] = relationship(
        back_populates="resource_pool_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )
    resource_specification: Mapped[list[models.ResourcePoolResourceSpecification]] = relationship(
        back_populates="resource_pool_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )
    resource_pool_resource: Mapped[list[models.ResourcePoolResource]] = relationship(
        back_populates="resource_pool_capacity", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )

    resource_pool_id: Mapped[str] = mapped_column(ForeignKey("resource_pool.id"))
    resource_pool: Mapped["ResourcePool"] = relationship(back_populates="capacity")

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePoolCapacity) -> "ResourcePoolCapacity":
        print("resource_capacity_schema", schema)
        applicable_time_period = models.ResourcePoolApplicableTimePeriod.from_schema(schema.applicable_time_period)
        related_party = models.ResourcePoolRelatedParty.from_schema(schema.related_party)
        print(type(related_party.id))
        place = [
            models.ResourcePoolPlace.from_schema(place)
            for place in schema.place
        ]
        resource_specification = [
            models.ResourcePoolResourceSpecification.from_schema(resource_spec)
            for resource_spec in schema.resource_specification
        ]
        resource_pool_resource = [
            models.ResourcePoolResource.from_schema(resource)
            for resource in schema.resource
        ]
        print(type(resource_specification))
        # resource_pool_capacity_id = str(uuid.uuid4())

        return cls(
            id=str(uuid.uuid4()),
            capacity_amount=schema.capacity_amount,
            capacity_amount_from=schema.capacity_amount_from,
            capacity_amount_remaining=schema.capacity_amount_remaining,
            capacity_amount_to=schema.capacity_amount_to,
            range_interval=schema.range_interval,
            applicable_time_period=applicable_time_period,
            related_party=related_party,
            place=place,
            resource_specification=resource_specification,
            resource_pool_resource=resource_pool_resource
        )




