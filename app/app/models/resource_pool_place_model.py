from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Capacity


class ResourcePlace(Base):
    id: Mapped[int] = mapped_column(
        String(255), primary_key=True, index=True, default=True
    )
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))

    capacity_id: Mapped[str] = mapped_column(ForeignKey("capacity.id"))
    capacity: Mapped["Capacity"] = relationship(back_populates="place")

    # capacity: Mapped["Capacity"] = relationship(
    #     back_populates="place", uselist=False)
