from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationResourceCapacity(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )

    type: str | None = Field(
        None,
        alias="@type",
        description="When sub-classing, this defines the super-class",
    )
    capacity_demand_amount: str | None = Field(
        None,
        alias="capacityDemandAmount",
        description="When sub-classing, this defines the super-class",
    )
    reservation_applicable_time_period: schemas.ReservationApplicableTimePeriod = Field(
        alias="applicableTimePeriod",
        description="Array of objects (RelatedParty)",
    )
    reservation_place: list[schemas.Place] = Field(
        alias="place",
        default_factory=list, description="Array of objects (Note)"
    )
    resource_pool: schemas.ReservationResourcePool = Field(
        alias="resourcePool",
        description="Array of objects (RelatedParty)",
    )
