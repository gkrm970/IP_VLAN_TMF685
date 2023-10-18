from pydantic import BaseModel, ConfigDict, Field


class RelatedParty(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )

    name: str | None = Field(None, description="Name of the related entity")
    role: str | None = Field(None, description="Role played by the related party")
