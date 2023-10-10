import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceRef(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    object_id: str | None = Field(None, alias="id", description="Identifier of the Resource")
    name: str | None = Field(None, description="Name of the resource collection")
    href: str | None = Field(None, description="Hyperlink to access the Resource")
    description: str | None = Field(None, description="Description of the Resource")