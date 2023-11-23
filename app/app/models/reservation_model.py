import uuid
from datetime import datetime
from typing import Any, Type
from urllib.parse import urljoin

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    InstrumentedAttribute,
    ColumnProperty,
)

from app import models, schemas, settings
from app.db.base import BaseDbModel

_ALL_DELETE_ORPHAN = "all, delete-orphan"


class Reservation(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))
    related_parties: Mapped[models.ReservationRelatedParty] = relationship(
        back_populates="reservation",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
        uselist=False,
    )
    requested_period: Mapped[models.ReservationRequestedPeriod] = relationship(
        back_populates="reservation",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
        uselist=False,
    )
    reservation_item: Mapped[list[models.ReservationItem]] = relationship(
        back_populates="reservation", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )
    reservation_state: Mapped[str | None] = mapped_column(String(255))
    valid_for: Mapped[models.ValidFor] = relationship(
        back_populates="reservation",
        lazy="selectin",
        cascade=_ALL_DELETE_ORPHAN,
        uselist=False,
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationCreate, reservation_state: str,
                    valid_for: datetime, href, _id, vlans) -> "Reservation":
        reservation_id = str(uuid.uuid4())
        related_parties = models.ReservationRelatedParty.from_schema(
            schema.related_parties
        )
        requested_period = models.ReservationRequestedPeriod.from_schema(schema.requested_period)
        sub_reservation_state = "completed"
        characteristic = []
        for vlan in vlans:
            characteristic_dict = [models.Characteristic.from_schema(ipv4_subnet="",
                                                                     ipv6_subnet="",
                                                                     vlan_8021q=str(vlan))]
            characteristic.append(characteristic_dict)

        reservation_resource = [
            models.ReservationResource.from_schema(href=href,
                                                   resource_id=_id,
                                                   characteristic=characteristic,
                                                   referred_type="ipv4Subnet",
                                                   )
        ]

        demand_amount = schema.reservation_item[0].reservation_resource_capacity.capacity_demand_amount

        applied_capacity_amount = models.AppliedCapacityAmount.from_schema(
            applied_capacity_amount=demand_amount, reservation_resource=reservation_resource
        )

        print("sub_reservation_state", sub_reservation_state)
        reservation_item_list = [
            models.ReservationItem.from_schema(reservation_item, sub_reservation_state=sub_reservation_state,
                                               applied_capacity_amount=applied_capacity_amount)
            for reservation_item in schema.reservation_item
        ]
        valid_for_instance = models.ValidFor.from_schema(valid_for)

        print("reservation_item_list", reservation_item_list)

        return cls(
            id=reservation_id,
            href=f"reservation/{reservation_id}",
            type=schema.type,
            related_parties=related_parties,
            requested_period=requested_period,
            reservation_item=reservation_item_list,
            reservation_state=reservation_state,
            valid_for=valid_for_instance
        )

    def to_dict(self, include: set[str] | None = None) -> dict[str, Any]:
        data = schemas.Reservation.model_validate(self).model_dump(
            by_alias=True, include=include
        )

        data["href"] = urljoin(
            f"{urljoin(str(settings.API_BASE_URL), settings.API_PREFIX)}/",
            self.href,
        )

        return data

    def update(self, update_schema: schemas.ReservationUpdate) -> None:
        # Any field that the client did not set in the API request will be excluded
        for field_name in update_schema.model_dump(exclude_unset=True).keys():
            # Get the column/relationship attributes from the model class (type(self)),
            # and not the instance itself that is retrieved from the DB
            model_attr: InstrumentedAttribute = getattr(type(self), field_name)

            update_schema_value = getattr(update_schema, field_name)

            if isinstance(model_attr.property, ColumnProperty):
                setattr(self, field_name, update_schema_value)

            # If the attribute is not a column property, the update has to create new
            # related model instances, instead of just assigning the value from the API
            # request. There are 1-to-1 and 1-to-many scenarios, which are
            # differentiated by the `uselist` attribute of the relationship.
            else:
                model_relationship: Relationship = model_attr.property  # type: ignore

                # The related model class is defined in the argument property of the relationship
                related_model_class: Type[
                    models.Reservation
                ] = model_relationship.argument

                if model_relationship.uselist:
                    update_model = [
                        related_model_class.from_schema(schema)  # type: ignore
                        for schema in update_schema_value
                    ]
                else:
                    update_model = related_model_class.from_schema(update_schema_value)  # type: ignore

                setattr(self, field_name, update_model)
