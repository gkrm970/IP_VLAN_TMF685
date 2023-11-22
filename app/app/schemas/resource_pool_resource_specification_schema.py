from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourcePoolResourceSpecification(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    type: str | None = Field(None, alias="@type", description=_NAME_DESCRIPTION)
    href: str = Field(..., description=_NAME_DESCRIPTION)
    resource_specification_id: str = Field(..., description=_NAME_DESCRIPTION)
