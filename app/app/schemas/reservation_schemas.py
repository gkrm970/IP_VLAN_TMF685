from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationBase(BaseModel):
    type: str | None = Field(
        None,
        alias="@type",
        description="When sub-classing, this defines the super-class",
    )

    related_parties: schemas.RelatedParty | None = Field(
        None,
        alias="relatedParty",
        description="Array of objects (RelatedParty)",
    )
    reservation_item: list[schemas.ReservationItem] | None = Field(
        default_factory=list, alias="reservationItem", description="Array of objects (Note)"
    )
    reservation_state: str | None = Field(None,alias="reservationState", description="state of the reservation")

    valid_for: schemas.ValidFor | None = Field(
        None,
        description="Array of objects (RelatedParty)",
    )


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )
    href: str = Field(..., description="The URI for the object itself.")
    type: str | None = Field(
        None,
        alias="@type",
        description="When sub-classing, this defines the super-class",
    )

    related_parties: schemas.RelatedParty = Field(
        alias="relatedParty",
        description="Array of objects (RelatedParty)",
    )
    reservation_item: list[schemas.ReservationItem] = Field(
        default_factory=list, alias="reservationItem", description="Array of objects (Note)"
    )
    reservation_state: str | None = Field(None, alias="reservationState", description="state of the reservation")

    # valid_for: schemas.ValidFor = Field(
    #     description="Array of objects (RelatedParty)",
    # )
    valid_for: schemas.ValidFor | dict | None = Field(
        None,
        description="Array of objects (RelatedParty)",
    )


