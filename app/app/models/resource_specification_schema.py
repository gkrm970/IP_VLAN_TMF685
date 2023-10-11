import uuid

from sqlalchemy import Date, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app import schemas
from app.db.base import Base


class ResourceSpecification(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str | None] = mapped_column(String(255))
    default_quantity: Mapped[int | None] = mapped_column(Integer)
    maximum_quantity: Mapped[int | None] = mapped_column(Integer)
    minimum_quantity: Mapped[int | None] = mapped_column(Integer)
    name: Mapped[str | None] = mapped_column(String(255))
    relationship_type: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str | None] = mapped_column(String(255))

    @classmethod
    def from_schema(cls, schema: schemas.ResourceSpecificationCreate) -> "ResourceSpecification":
        resource_pool_id = str(uuid.uuid4())
        return cls(
            id=resource_pool_id,
            href=schema.href,
            default_quantity=schema.default_quantity,
            maximum_quantity=schema.maximum_quantity,
            minimum_quantity=schema.minimum_quantity,
            name=schema.name,
            relationship_type=schema.relationship_type,
            role=schema.role
        )

    def to_dict(self) -> schemas.ResourceSpecification:
        return schemas.ResourceSpecification.model_validate(self)

