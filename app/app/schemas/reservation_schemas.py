from pydantic import BaseModel, ConfigDict, Field

from app import schemas


class ReservationBase(BaseModel):
    schema_location: str = Field(None, alias="@schemaLocation",
                                 description="A link to the schema describing a resource.")
    type: str = Field(None, alias="@type", description="The type of the resource.")
    href: str = Field(None, description="The URI for the object itself.")
    reservation_state: str = Field(None, description="The state of the reservation.")
    valid_for: str = Field(None, description="The period for which the object is valid.")
    base_type: str = Field(None, alias="@baseType", description="The base type of the resource.")
    description: str = Field(None, description="Description of the reservation.")
    related_party: schemas.RelatedPartyRef = Field(None, description="A related party associated with this resource.")
    product_offering: schemas.ProductOfferingRef = Field(None,
                                                         description="A product offering represents entities that are "
                                                                     "order-able from the provider of the catalog, "
                                                                     "this resource includes pricing information.")


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
