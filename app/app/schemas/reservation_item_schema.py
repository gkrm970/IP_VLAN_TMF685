from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    quantity: int | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    reservation_resource_capacity: schemas.ReservationResourceCapacity = Field(
        alias="resourceCapacity",
        description="Array of objects (RelatedParty)",
    )
