import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class RequestedPeriod(Base):
    __tablename__ = 'requested_period'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    daysOfWeek: Mapped[str] = mapped_column(String(255))
    fromToDateTime: Mapped[DateTime] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))
    validFor: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with Reservation table and RequestedPeriod table (RequestedPeriod table is child)
    reservation_id: Mapped[str] = mapped_column(String), ForeignKey("reservation.id")
    reservation = relationship("Reservation", back_populates="requested_period")  # 1..0..1

