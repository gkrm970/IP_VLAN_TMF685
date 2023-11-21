from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationItemBase(BaseModel):

    quantity: int | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    reservation_resource_capacity: schemas.ReservationResourceCapacity = Field(
        alias="resourceCapacity",
        description="Array of objects (RelatedParty)",
    )


class ReservationItemCreate(ReservationItemBase):
    pass


class ReservationItemUpdate(ReservationItemBase):
    pass


class ReservationItem(ReservationItemBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )
    applied_capacity_amount: schemas.AppliedCapacityAmount = Field(
        alias="appliedCapacityAmount",
        description="Array of objects (RelatedParty)",
    )
    quantity: int | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    reservation_resource_capacity: schemas.ReservationResourceCapacity = Field(
        alias="resourceCapacity",
        description="Array of objects (RelatedParty)",
    )
    sub_reservation_state: str | None = Field(None, alias="subReservationState", description=_NAME_DESCRIPTION)
