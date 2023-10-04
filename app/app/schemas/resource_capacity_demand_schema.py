from pydantic import BaseModel, Field

from app import schemas


class ResourceCapacityDemand(BaseModel):
    resourceCapacityDemandAmount: str | None = Field(None, description="The amount of the resource capacity demand.")
    applicableTimePeriod: schemas.ApplicableTimePeriod | None = Field(None,
                                                              description="The period for which the object is valid.")
    place: schemas.PlaceRef | None = Field(None, description="A place is a spatial area defined by a set of coordinates.")
    resourcePool: schemas.ResourcePool | None = Field(None, description="A resource pool is a collection of resources.")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")

