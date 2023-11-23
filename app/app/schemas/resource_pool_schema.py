from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourcePoolBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str | None = Field(None, description=_NAME_DESCRIPTION)

    type: str | None = Field(
        None,
        alias="@type",
        description=(
            "Category of the concrete resource, "
            "e.g Gold, Silver for MSISDN concrete resource"
        ),
    )
    description: str | None = Field(
        None, description="Free-text description of the resource"
    )


class ResourcePoolCreate(ResourcePoolBase):
    type: str = Field(
        alias="@type",
        description=(
            "Category of the concrete resource, "
            "e.g Gold, Silver for MSISDN concrete resource"
        ),
    )

    capacity: list[schemas.ResourcePoolCapacityCreate] = Field(
        default_factory=list,
        description="Configuration features",
    )


class ResourcePoolUpdate(ResourcePoolBase):
    pass


class ResourcePool(ResourcePoolBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type"
        ),
    )
    capacity: list[schemas.ResourcePoolCapacity] = Field(
        default_factory=list,
        description="Configuration features",
    )
