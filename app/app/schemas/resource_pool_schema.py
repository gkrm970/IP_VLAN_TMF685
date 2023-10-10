import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas


class ResourcePool(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(None, description="Identifier of the Resource Pool.")
    href: str | None = Field(None, description="Hyperlink to access the Resource Pool.")
    description: str | None = Field(None, description="Description of the Resource Pool.")
    related_party: str | None = Field(None, alias="relatedParty",
                                      description="A related party defines party or party role linked to a "
                                                  "specific entity, who uses the resource of Resource Pool. ")

    resource_collection: str | None = Field(None, alias="resourceCollection", description="an aggregate entity "
                                                                                          "consisting of "
                                                                                          "ResourceElement")
    base_type: str | None = Field(None, alias="@baseType", description="Generic attribute indicating the base class "
                                                                       "type of the"
                                                                       "extension class of the current object. Useful "
                                                                       "only when the class"
                                                                       "type of the current object is unknown to the "
                                                                       "implementation. ")
    schema_location: str | None = Field(None, alias="@schemaLocation",
                                        description=" Generic attribute containing the link to the schema that"
                                                    "defines the structure of the class type of the current object.")
    type: str | None = Field(None, alias="@type", description="Type of the Resource Pool.")

    # ResourcePool and ResourceRef are one-to-many relationship(ResourceRef  is child of ResourcePool)
    resource_ref: schemas.ResourceRef | None = Field(None, alias="resource",
                                                                       description="Reference of the "
                                                                                   "ResourceCollection.")
