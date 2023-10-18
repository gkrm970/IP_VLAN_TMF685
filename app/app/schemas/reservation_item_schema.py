from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    quantity: int | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    sub_reservation_state: str | None = Field(
        None,
        alias="subReservationState",
        description="When sub-classing, this defines the super-class",
    )
    applied_capacity_amount: schemas.AppliedCapacityAmount = Field(
        alias="appliedCapacityAmount",
        description="Array of objects (RelatedParty)",
    )
    reservation_resource_capacity: schemas.ReservationResourceCapacity = Field(
        alias="resourceCapacity",
        description="Array of objects (RelatedParty)",
    )

