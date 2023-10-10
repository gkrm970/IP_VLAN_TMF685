import uuid
from datetime import date
from typing import Any

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
    requested_period_ref: Mapped[models.RequestedPeriod | None] = relationship(back_populates="reservation",
                                                                               lazy="selectin",
                                                                               cascade="all, delete-orphan",
                                                                               uselist=False)
    reservation_item_ref: Mapped[list[models.ReservationItem]] = relationship(back_populates="reservation",
                                                                              lazy="selectin",
                                                                              cascade="all, delete-orphan",
                                                                              uselist=True
                                                                              )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationCreate) -> "Reservation":
        reservation_id = str(uuid.uuid4())
        reservation_item_ref = [models.ReservationItem.from_schema(reservation_item) for reservation_item in
                                schema.reservation_item_ref]

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
            requested_period_ref=models.RequestedPeriod.from_schema(schema.requested_period_ref),
            reservation_item_ref=reservation_item_ref

        )

    def to_dict(self, include_fields: set[str] | None = None) -> dict[str, Any]:
        """
        Converts the Reservation object to a schema dictionary.

        Args:
            include_fields (set[str] | None): Optional set of fields to include in the schema.

        Returns:
            dict[str, Any]: The schema dictionary representing the Reservation object.
        """
        try:
            return schemas.Reservation.model_validate(self).model_dump(
                by_alias=True, include=include_fields
            )
        except Exception as e:
            # Handle the exception here, e.g. log the error or return a default value
            return {}
