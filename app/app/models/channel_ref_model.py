import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class ChannelRef(Base):
    __tablename__ = 'channel_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    referredType: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with Reservation table and ChannelRef table (ChannelRef table is child)
    reservation_id: Mapped[str] = mapped_column(String), ForeignKey("reservation.id")
    reservation = relationship("Reservation", back_populates="channel_ref")  # 1..0..1
