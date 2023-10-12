from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Capacity


class ResourceRelatedParty(Base):
    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, index=True, default=True
    )
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))

    capacity_id: Mapped[str] = mapped_column(ForeignKey("capacity.id"))
    capacity: Mapped["Capacity"] = relationship(back_populates="related_party")

    # capacity: Mapped["Capacity"] = relationship(
    #     back_populates="related_party", uselist=False)
