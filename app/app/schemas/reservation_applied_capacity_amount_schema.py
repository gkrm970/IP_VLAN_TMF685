from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class AppliedCapacityAmount(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    applied_capacity_amount: str | None = Field(
        None, alias="appliedCapacityAmount", description=_NAME_DESCRIPTION
    )

    reservation_resource: list[schemas.ReservationResource] | None = Field(
        None,
        alias="resource",
        # default_factory=list,
        description="Configuration features",
    )
