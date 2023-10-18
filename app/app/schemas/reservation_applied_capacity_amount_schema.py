from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class AppliedCapacityAmount(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )
    applied_capacity_amount: str | None = Field(
        None,
        alias="appliedCapacityAmount",
        description="When sub-classing, this defines the super-class",
    )
    reservation_resource: list[schemas.Resource] = Field(
        alias="resource",
        default_factory=list, description="Array of objects (Note)"
    )
