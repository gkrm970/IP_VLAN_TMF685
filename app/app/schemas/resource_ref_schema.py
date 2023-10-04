from pydantic import BaseModel, Field


class ResourceRef(BaseModel):
    id: str | None = Field(None, description="Identifier of the resource.")
    href: str | None = Field(None, description="The URI for the object itself.")
    value: str | None = Field(None, description="The value of the resource.")
    referred_type: str | None = Field(None, alias="@referredType",
                                      description="The actual type of the target instance.")

