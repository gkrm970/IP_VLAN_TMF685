from typing import List
from pydantic import BaseModel, ConfigDict, Field
from app import schemas


class ResourceRelatedParty(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(None, description="Identifier of the Resource Pool.")
    name: str | None = Field(None, description="A value and units that define the CapacityAmount, such as "
                                               "10000 ea, 10B Mb. ")
    role: str | None = Field(None, description="Name of the resource collection")
