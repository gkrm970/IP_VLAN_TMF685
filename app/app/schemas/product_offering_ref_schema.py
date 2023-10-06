from pydantic import BaseModel, ConfigDict, Field


class ProductOfferingRef(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    href: str | None = Field(None, description="Reference of the product offering.")
    id: str | None = Field(None, description="Identifier of the product offering.")
    name: str | None = Field(None, description="Name of the product offering.")
    referred_type: str | None = Field(
        None,
        alias="@referredType",
        description=". Indicates the type of the referred object. This attribute is to be used when the object is "
                    "representing a reference to an existing object instead of the of the object itself.",)
