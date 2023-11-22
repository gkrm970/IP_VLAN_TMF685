import uuid
from typing import Any
from urllib.parse import urljoin

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship, InstrumentedAttribute, ColumnProperty,
)
from app import models, settings
from app.db.base import BaseDbModel
from app import schemas

# Cascade rule for SQLAlchemy relationship. The all symbol is a synonym for save-update,
# merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan
# indicates that the child object should follow along with its parent in all cases, and
# be deleted once it is no longer associated with that parent
_ALL_DELETE_ORPHAN = "all, delete-orphan"


class ResourcePool(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    capacity: Mapped[list[models.ResourcePoolCapacity]] = relationship(
        back_populates="resource_pool", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePoolCreate) -> "ResourcePool":
        resource_pool_id = str(uuid.uuid4())
        capacity = [
            models.ResourcePoolCapacity.from_schema(capacity)
            for capacity in schema.capacity
        ]
        print("capacity_response", capacity)
        return cls(
            id=resource_pool_id,
            href=f"resource/{resource_pool_id}",
            name=schema.name,
            description=schema.description,
            type=schema.type,
            capacity=capacity

        )

    def to_dict(self, include: set[str] | None = None) -> dict[str, Any]:
        data = schemas.ResourcePool.model_validate(self).model_dump(
            by_alias=True, include=include
        )

        data["href"] = urljoin(
            f"{urljoin(str(settings.API_BASE_URL), settings.API_PREFIX)}/",
            self.href,
        )

        return data

    def update(self, update_schema: schemas.ResourcePoolUpdate) -> None:
        # Any field that the client did not set in the API request will be excluded
        for field_name in update_schema.model_dump(exclude_unset=True).keys():
            # Get the column/relationship attributes from the model class (type(self)),
            # and not the instance itself that is retrieved from the DB
            model_attr: InstrumentedAttribute = getattr(type(self), field_name)

            update_schema_value = getattr(update_schema, field_name)

            if isinstance(model_attr.property, ColumnProperty):
                setattr(self, field_name, update_schema_value)

            # If the attribute is not a column property, the update has to create new
            # related model instances, instead of just assigning the value from the API
            # request. There are 1-to-1 and 1-to-many scenarios, which are
            # differentiated by the `uselist` attribute of the relationship.
            else:
                model_relationship: Relationship = model_attr.property  # type: ignore

                # The related model class, e.g. models.Note or models.Feature is defined
                # in the argument property of the above Relationship object
                related_model_class = model_relationship.argument

                if model_relationship.uselist:
                    update_model = [
                        related_model_class.from_schema(schema)  # type: ignore
                        for schema in update_schema_value
                    ]

                else:
                    update_model = related_model_class.from_schema(  # type: ignore
                        update_schema_value
                    )

                setattr(self, field_name, update_model)
