import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class ReservationItem(Base):
    __tablename__ = 'reservation_item'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[str] = mapped_column(String(255))
    subReservationState: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and ReservationItem table (ReservationItem table is child)
    reservation_id: Mapped[str] = mapped_column(String), ForeignKey("reservation.id")
    reservation_item = relationship("ReservationItem", back_populates="reservation_item")  # 1..1

    # 1..0 relationship with ReservationItem table and AppliedCapacityAmount table (ReservationItem table is parent)
    applied_capacity_amount = relationship(models.AppliedCapacityAmount, back_populates="reservation_item")

    # 1..1 relationship with ReservationItem table and ResourceCapacityDemand table (ReservationItem table is parent)
    resource_capacity_demand = relationship(models.ResourceCapacityDemand, back_populates="reservation_item")  # 1..1
