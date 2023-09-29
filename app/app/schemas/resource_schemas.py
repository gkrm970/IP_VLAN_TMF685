from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourceBase(BaseModel):
    baseType: str = Field(None, alias="@baseType", description="The base type of the resource.")
    schemaLocation: str = Field(None, alias="@schemaLocation", description="A link to the schema describing a resource.")
    type: str = Field(None, alias="@type", description="The type of the resource.")
    relatedParty: str = Field(None, description="A related party associated with this resource.")
    href: str = Field(None, description="The URI for the object itself.")
    description: str = Field(None, description="A narrative text describing the resource.")


class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    pass


class Resource(ResourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )