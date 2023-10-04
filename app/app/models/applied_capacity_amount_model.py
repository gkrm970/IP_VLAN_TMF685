import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class AppliedCapacityAmount(Base):
    __tablename__ = 'applied_capacity_amount'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[int] = mapped_column(String(255))
    appliedDemandAmount: Mapped[str] = mapped_column(String(255))

    # 1..0 relationship with ReservationItem table and AppliedCapacityAmount table (AppliedCapacityAmount table is
    # child)
    reservation_item_id: Mapped[str] = mapped_column(String), ForeignKey("reservation_item.id")
    reservation_item = relationship("ReservationItem", back_populates="applied_capacity_amount")

    # 0..1 ..0..* relationship with AppliedCapacityAmount table and ResourceRef table (AppliedCapacityAmount table is
    # parent)
    resource_ref = relationship("ResourceRef", back_populates="applied_capacity_amount")
