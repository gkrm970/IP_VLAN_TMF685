from pydantic import BaseModel, Field

from app import schemas


class ResourceReservationItem(BaseModel):
    quantity: str
    resourceCapacityDemand: list[ResourceCapacityDemand] | None = Field(None,
                                                                        description="The resource capacity demand.")
