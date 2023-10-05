import uuid
from datetime import date

from sqlalchemy import Date, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas
from app.db.base import Base


class Reservation(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str | None] = mapped_column(String(255))
    base_type: Mapped[str | None] = mapped_column(String(255))
    schema_location: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    reservation_state: Mapped[str | None] = mapped_column(String(255))
    valid_for: Mapped[date] = mapped_column(Date, server_default=func.now())

    related_party_ref: Mapped[models.RelatedPartyRef] = relationship(
        back_populates="reservation", lazy="selectin", cascade="all, delete-orphan", uselist=False
    )

    product_offering_ref: Mapped[models.ProductOfferingRef | None] = relationship(
        back_populates="reservation", lazy="selectin", cascade="all, delete-orphan", uselist=False
    )

    channel_ref: Mapped[models.ChannelRef | None] = relationship(
        back_populates="reservation", lazy="selectin", cascade="all, delete-orphan", uselist=False
    )

    # 1..0..1 relationship with Reservation table and RequestedPeriod table (Reservation table is parent)
    # requested_period = relationship("RequestedPeriod", back_populates="reservation", uselist=True)  # 1..0..1
    #
    # # 1..0..1 relationship with Reservation table and ChannelRef table (Reservation table is parent)
    # channel_ref = relationship("ChannelRef", back_populates="reservation", uselist=True)  # 1..0..1
    #
    # # 1..1..* relationship with Reservation table and ReservationItem table (Reservation table is parent)
    # reservation_item = relationship("ReservationItem", back_populates="reservation", uselist=True)  # 1..1..*

    @classmethod
    def from_schema(cls, schema: schemas.ReservationCreate) -> "Reservation":
        reservation_id = str(uuid.uuid4())

        return cls(
            id=reservation_id,
            href=f"reservation/{reservation_id}",
            base_type=schema.base_type,
            schema_location=schema.schema_location,
            type=schema.type,
            description=schema.description,
            reservation_state=schema.reservation_state,
            valid_for=schema.valid_for,
            product_offering_ref=models.ProductOfferingRef.from_schema(
                schema.product_offering_ref
            ),
            related_party_ref=models.RelatedPartyRef.from_schema(
                schema.related_party_ref,
            ),
            channel_ref=models.ChannelRef.from_schema(schema.channel_ref),
        )

    def to_schema(self) -> schemas.Reservation:
        return schemas.Reservation.model_validate(self)
