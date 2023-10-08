import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas


class ReservationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    schema_location: str = Field(
        None,
        alias="@schemaLocation",
        description="A link to the schema describing a resource.",
    )
    type: str = Field(None, alias="@type", description="The type of the resource.")
    reservation_state: str = Field(None, description="The life cycle state of the reservation.")
    valid_for: datetime.date = Field(
        default_factory=datetime.date.today, description="The period for which the object is valid."
    )
    base_type: str = Field(
        None, alias="@baseType", description="The base type of the resource."
    )
    description: str = Field(None, description="Description of the reservation.")
    related_party_ref: schemas.RelatedPartyRef = Field(
        ...,
        alias="relatedParty",
        description=" A related party defines party or party role linked to a specific entity.",
    )
    product_offering_ref: schemas.ProductOfferingRef | None = Field(
        None,
        alias="productOffering",
        description="A product offering represents entities that are "
                    "order-able from the provider of the catalog, "
                    "this resource includes pricing information.",
    )
    channel_ref: schemas.ChannelRef | None = Field(
        None,
        alias="channel", description="The channel defines the channel for selling product offerings")
    requested_period_ref: schemas.RequestedPeriod | None = Field(alias="requestedPeriod", description="The requested "
                                                                                                      "period for the "
                                                                                                      "reservation.")
    reservation_item_ref: list[schemas.ReservationItem] = Field(..., alias="reservationItem", description="The "
                                                                                                           "reservation"
                                                                                                           "item "
                                                                                                           "associated "
                                                                                                           "with the "
                                                                                                           "reservation.")


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )
    href: str = Field(None, description="The URI for the object itself.")
    # href: str = Field(None, description="The URI for the object itself.")
    # name: str = Field(None, description="A string used to give a name to the resource")
