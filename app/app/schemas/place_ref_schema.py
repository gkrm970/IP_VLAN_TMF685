from pydantic import BaseModel, Field


class PlaceRef(BaseModel):
    id: str | None = Field(None, description="Identifier of the place.")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")
    name: str | None = Field(None, description="Name of the place.")

