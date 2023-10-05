import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ProductOfferingRef(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referred_type: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and ProductOfferingRef table (ProductOfferingRef table is child)
    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"))
    reservation: Mapped["Reservation"] = relationship(back_populates="product_offering_ref")  # 1..1

    @classmethod
    def from_schema(cls, schema: schemas.ProductOfferingRef) -> "ProductOfferingRef":
        return cls(**schema.model_dump())
