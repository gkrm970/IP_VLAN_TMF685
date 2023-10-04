import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ProductOfferingRef(Base):
    __tablename__ = 'product_offering_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referred_type: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and ProductOfferingRef table (ProductOfferingRef table is child)
    reservation_id: Mapped[str] = mapped_column(String), ForeignKey("reservation.id")
    reservation: Mapped["Reservation"] = relationship(back_populates="product_offering_ref")  # 1..1
