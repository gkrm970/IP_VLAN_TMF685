from pydantic import BaseModel, Field

from app import schemas


class ResourcePool(BaseModel):
    id: str | None = Field(None, description="Identifier of the resource pool.")
    href: str | None = Field(None, description="The URI for the object itself.")
    resource: schemas.ResourceRef | None = Field(None, description="A resource is an identifiable physical or logical "
                                                                   "resource.")

