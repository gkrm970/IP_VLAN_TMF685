import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel

# Cascade rule for SQLAlchemy relationship. The all symbol is a synonym for save-update,
# merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan
# indicates that the child object should follow along with its parent in all cases, and
# be deleted once it is no longer associated with that parent
_ALL_DELETE_ORPHAN = "all, delete-orphan"
if TYPE_CHECKING:
    from app.models import ResourcePoolCapacity


class ResourcePoolResourceSpecification(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)

    type: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    resource_specification_id: Mapped[str] = mapped_column(String(255))

    resource_pool_capacity_id: Mapped[str] = mapped_column(
        ForeignKey("resource_pool_capacity.id")
    )
    resource_pool_capacity: Mapped["ResourcePoolCapacity"] = relationship(
        back_populates="resource_specification"
    )

    @classmethod
    def from_schema(
        cls, schema: schemas.ResourcePoolResourceSpecification
    ) -> "ResourcePoolResourceSpecification":
        return cls(
            id=str(uuid.uuid4()),
            type=schema.type,
            href=schema.href,
            resource_specification_id=schema.resource_specification_id,
        )
