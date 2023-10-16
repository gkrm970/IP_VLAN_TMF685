import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceRef(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description=(
            "Identifier of the note within its containing entity "
            "(may or may not be globally unique, depending on provider implementation)"
        ),
    )

    object_id: str | None = Field(None, description="Identifier of the Resource")
    name: str | None = Field(..., description="Name of the resource collection")
    href: str | None = Field(None, description="Hyperlink to access the Resource")
    description: str | None = Field(None, description="Description of the Resource")