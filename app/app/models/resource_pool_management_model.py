import uuid
from typing import TYPE_CHECKING, Optional, Any
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app import schemas, models

# if TYPE_CHECKING:
#     from app.models import Capacity


class ResourcePoolManagement(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    resource_capacity: Mapped[list[models.Capacity]] = relationship(
        back_populates="resource_pool_management", lazy="selectin", cascade="all, delete-orphan"
    )

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePoolManagementCreate) -> "ResourcePoolManagement":
        resource_pool_id = str(uuid.uuid4())

        print(f'{resource_pool_id}')

        resource_capacity = [
            models.Capacity.from_schema(capacities)
            for capacities in schema.resource_capacity
        ]
        print(f'{resource_capacity=}')
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
            href= f"resourcePool/{resource_pool_id}",
            type=schema.type,
            name=schema.name,
            resource_capacity=resource_capacity
        )

    def to_dict(self) -> schemas.ResourcePoolManagement:
        return schemas.ResourcePoolManagement.model_validate(self)
