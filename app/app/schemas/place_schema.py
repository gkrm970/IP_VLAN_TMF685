from pydantic import BaseModel, ConfigDict, Field


class ResourcePlace(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    # id: str | None = Field(
    #     None, description="Identifier of the place."
    # )
    name: str | None = Field(
        None, description="Identifier of the place."
    )
    type: str | None = Field(
        None, description="Identifier of the place."
    )