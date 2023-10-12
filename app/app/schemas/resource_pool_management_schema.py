

from pydantic import BaseModel, ConfigDict, Field

from app import schemas


class ResourcePoolManagementBase(BaseModel):

    # id: str | None = Field(None, description="Identifier of the Resource Pool.")
    # href: str | None = Field(None, description="Hyperlink to access the Resource Pool.")
    type: str | None = Field(None, alias="@type", description="Type of the Resource Pool.")
    name: str | None = Field(None, description="name of the Resource Pool.")

    resource_capacity: list[schemas.ResourceCapacity] | None = Field(
        ...,
        alias="capacity",
        description=" A related party defines party or party role linked to a specific entity.",
    )


class ResourcePoolManagementCreate(ResourcePoolManagementBase):
    pass


class ResourcePoolManagementUpdate(ResourcePoolManagementBase):
    pass


class ResourcePoolManagement(ResourcePoolManagementBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(None, description="Identifier of the Resource Pool.")
    href: str | None = Field(None, description="Hyperlink to access the Resource Pool.")
    type: str | None = Field(None, alias="@type", description="Type of the Resource Pool.")
    name: str | None = Field(None, description="name of the Resource Pool.")

    resource_capacity: list[schemas.ResourceCapacity] | None = Field(
        None,
        alias="capacity",
        description=" A related party defines party or party role linked to a specific entity.",
    )