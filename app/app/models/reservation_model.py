import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class Reservation(Base):
    __tablename__ = 'reservation'
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    base_type: Mapped[str | None] = mapped_column(String(255))
    schema_location: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))
    href: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    reservation_state: Mapped[str | None] = mapped_column(String(255))
    valid_for: Mapped[str | None] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and RelatedPartyRef table (Reservation table is parent)
    related_party_ref: Mapped[models.RelatedPartyRef] = relationship(back_populates="reservation",
                                                                           lazy="selectin",
                                                                           cascade="all, delete-orphan")  # 1..1

    # 1..1 relationship with Reservation table and ProductOfferingRef table (Reservation table is parent)
    product_offering_ref: Mapped[models.ProductOfferingRef] = relationship(back_populates="reservation",
                                                                                 lazy="selectin",
                                                                                 cascade="all, delete-orphan")  # 1..1

    # 1..0..1 relationship with Reservation table and RequestedPeriod table (Reservation table is parent)
    # requested_period = relationship("RequestedPeriod", back_populates="reservation", uselist=True)  # 1..0..1
    #
    # # 1..0..1 relationship with Reservation table and ChannelRef table (Reservation table is parent)
    # channel_ref = relationship("ChannelRef", back_populates="reservation", uselist=True)  # 1..0..1
    #
    # # 1..1..* relationship with Reservation table and ReservationItem table (Reservation table is parent)
    # reservation_item = relationship("ReservationItem", back_populates="reservation", uselist=True)  # 1..1..*
