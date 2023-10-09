from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette import status

from app import schemas, models
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Reservation


class ReservationItem(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    quantity: Mapped[int | None] = mapped_column(Integer)
    sub_reservation_state: Mapped[str | None] = mapped_column(String(255))
    applied_capacity_amount: Mapped[str | None] = mapped_column(String(255))
    base_type: Mapped[str | None] = mapped_column(String(255))
    schema_location: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))

    reservation_id: Mapped[str] = mapped_column(ForeignKey("reservation.id"), unique=True)
    reservation: Mapped["Reservation"] = relationship(
        back_populates="reservation_item_ref"
    )

    resource_capacity_demand_ref: Mapped[models.ResourceCapacityDemand | None] = relationship(
        back_populates="reservation_item", lazy="selectin", cascade="all, delete-orphan", uselist=False
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationItem) -> schemas.ReservationItem:
        """
        Create a `ReservationItem` object from a `ReservationItem` schema.

        Args:
        schema (schemas.ReservationItem): The schema representing a `ReservationItem`.

        Returns:
        ReservationItem: An instance of the `ReservationItem` class.
        """
        try:
            if not isinstance(schema, schemas.ReservationItem):
                raise ValueError("Invalid schema. Expected schemas.ReservationItem instance.")
            return ReservationItem(
                id=schema.id,
                quantity=schema.quantity,
                sub_reservation_state=schema.sub_reservation_state,
                applied_capacity_amount=schema.applied_capacity_amount,
                base_type=schema.base_type,
                schema_location=schema.schema_location,
                type=schema.type,
                resource_capacity_demand_ref=models.ResourceCapacityDemand.from_schema(schema.resource_capacity_demand_ref)
            )
        except Exception as e:
            raise ValueError(f"Failed to create ReservationItem from schema: {str(e)}, status code: {status.HTTP_500_INTERNAL_SERVER_ERROR}")
