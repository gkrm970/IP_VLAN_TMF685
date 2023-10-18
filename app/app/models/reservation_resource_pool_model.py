import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ReservationResourceCapacity


class ReservationResourcePool(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    pool_id: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))

    reservation_resource_capacity_id: Mapped[str] = mapped_column(ForeignKey("reservation_resource_capacity.id"))
    reservation_resource_capacity: Mapped["ReservationResourceCapacity"] = relationship(back_populates="resource_pool")

    @classmethod
    def from_schema(cls, schema: schemas.ReservationResourcePool) -> "ReservationResourcePool":
        schema.id = schema.id or str(uuid.uuid4())
        return cls(**schema.model_dump())

