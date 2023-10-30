import uuid
from typing import Type, Any
from urllib.parse import urljoin

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    InstrumentedAttribute,
    ColumnProperty,
)
from app.db.base import BaseDbModel
from app import schemas, models, settings

_ALL_DELETE_ORPHAN = "all, delete-orphan"


class ResourcePoolManagement(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    resource_capacity: Mapped[list[models.Capacity]] = relationship(
        back_populates="resource_pool_management",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
    )

    @classmethod
    def from_schema(
        cls, schema: schemas.ResourcePoolManagementCreate
    ) -> "ResourcePoolManagement":
        resource_pool_id = str(uuid.uuid4())

        resource_capacity = [
            models.Capacity.from_schema(capacities)
            for capacities in schema.resource_capacity
        ]
        """
        Create a ResourcePool object from a schema.

        Args:
            schema (schemas.ResourcePool | None): The schema to create the object from.

        Returns:
            Optional[ResourcePool]: The created ResourcePool object, or None if the schema is None.
        """
        # if schema is None:
        #     return None

        return cls(
            id=resource_pool_id,
            href=f"resourcePool/{resource_pool_id}",
            type=schema.type,
            name=schema.name,
            resource_capacity=resource_capacity,
        )

    def to_dict(self, include: set[str] | None = None) -> dict[str, Any]:
        data = schemas.ResourcePoolManagement.model_validate(self).model_dump(
            by_alias=True, include=include
        )

        data["href"] = urljoin(
            f"{urljoin(str(settings.API_BASE_URL), settings.API_PREFIX)}/",
            self.href,
        )
        return data

    def update(self, update_schema: schemas.ResourcePoolManagementUpdate) -> None:
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

                # The related model class is defined in the argument property of the relationship
                related_model_class: Type[
                    models.ResourcePoolManagement
                ] = model_relationship.argument

                if model_relationship.uselist:
                    update_model = [
                        related_model_class.from_schema(schema)  # type: ignore
                        for schema in update_schema_value
                    ]
                else:
                    update_model = related_model_class.from_schema(update_schema_value)  # type: ignore

                setattr(self, field_name, update_model)
