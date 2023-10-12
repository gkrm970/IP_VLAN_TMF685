from typing import List
from pydantic import BaseModel, ConfigDict, Field
from app import schemas


class ResourceCapacity(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    capacity_amount: int | None = Field(None, alias="capacityAmount", description="A value and units that define the CapacityAmount, such as "
                                                         "10000 ea, 10B Mb. ")
    capacity_amount_from: str | None = Field(None, alias="capacityAmountFrom", description="Name of the resource collection")
    capacity_amount_to: str | None = Field(None, alias="capacityAmountTo", description="Name of the resource collection")

    related_party: schemas.ResourceRelatedParty = Field(
        ...,
        alias="relatedParty",
        description=" A related party defines party or party role linked to a specific entity.",
    )
    place: List[schemas.ResourcePlace] | None = Field(
        None,
        description=" A related party defines party or party role linked to a specific entity.",
    )
