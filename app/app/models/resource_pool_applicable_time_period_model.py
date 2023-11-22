import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
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


class ResourcePoolApplicableTimePeriod(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    from_: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))

    resource_pool_capacity_id: Mapped[str] = mapped_column(
        ForeignKey("resource_pool_capacity.id")
    )
    resource_pool_capacity: Mapped["ResourcePoolCapacity"] = relationship(
        back_populates="applicable_time_period"
    )

    @classmethod
    def from_schema(
        cls, schema: schemas.ResourcePoolApplicableTimePeriod
    ) -> "ResourcePoolApplicableTimePeriod":
        return cls(id=str(uuid.uuid4()), from_=schema.from_)
