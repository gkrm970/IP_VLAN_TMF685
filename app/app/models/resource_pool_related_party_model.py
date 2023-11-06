import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from app import schemas
from app.db.base import BaseDbModel

# Cascade rule for SQLAlchemy relationship. The all symbol is a synonym for save-update,
# merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan
# indicates that the child object should follow along with its parent in all cases, and
# be deleted once it is no longer associated with that parent
_ALL_DELETE_ORPHAN = "all, delete-orphan"
if TYPE_CHECKING:
    from app.models import ResourcePoolCapacity


class ResourcePoolRelatedParty(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    party_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))

    resource_pool_capacity_id: Mapped[str] = mapped_column(ForeignKey("resource_pool_capacity.id"))
    resource_pool_capacity: Mapped["ResourcePoolCapacity"] = relationship(back_populates="related_party")

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePoolRelatedParty) -> "ResourcePoolRelatedParty":
        print("related_party", schema)
        # schema.id = schema.id or str(uuid.uuid4())

        # The base_type, schemaLocation and type fields are not in the OpenAPI spec, but
        # they are part of the UML diagram for this model, so we include them here even
        # though they are always going to be NULL in the DB
        return cls(
            **schema.model_dump()
        )
