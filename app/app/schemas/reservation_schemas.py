from pydantic import BaseModel, ConfigDict, Field

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
    requested_period: schemas.ReservationRequestedPeriod | None = Field(
        None,
        alias="requestedPeriod",
        description="Array of objects (RelatedParty)",
    )
    reservation_item: list[schemas.ReservationItem] | None = Field(
        default_factory=list,
        alias="reservationItem",
        description="Array of objects (Note)",
    )


class ReservationCreate(ReservationBase):
    related_parties: schemas.RelatedParty = Field(
        ...,
        alias="relatedParty",
        description="Array of objects (RelatedParty)",
    )


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
    reservation_state: str | None = Field(
        None,
        alias="reservationState",
        description="When sub-classing, this defines the super-class",
    )
    valid_for: schemas.ReservationValidFor | None = Field(
        None,
        description="Array of objects (RelatedParty)",
    )
