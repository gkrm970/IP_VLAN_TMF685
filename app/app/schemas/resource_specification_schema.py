from pydantic import BaseModel, ConfigDict, Field


class ResourceSpecificationBase(BaseModel):
    id: str | None = Field(None, alias="id", description="Identifier of the Resource")
    href: str | None = Field(None, description="Hyperlink to access the Resource")
    default_quantity: int | None = Field(None, alias="defaultQuantity", description="Default quantity of the Resource")
    maximum_quantity: int | None = Field(None, alias="maximumQuantity", description="Maximum quantity of the Resource")
    minimum_quantity: int | None = Field(None, alias="minimumQuantity", description="Minimum quantity of the Resource")
    name: str | None = Field(None, description="Name of the resource collection")
    relationship_type: str | None = Field(None, alias="relationshipType", description="Relationship type of the Resource")
    role: str | None = Field(None, description="Role of the Resource")


class ResourceSpecificationCreate(ResourceSpecificationBase):
    pass


class ResourceSpecificationUpdate(ResourceSpecificationBase):
    pass


class ResourceSpecification(ResourceSpecificationBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)