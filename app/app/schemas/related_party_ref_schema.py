from pydantic import BaseModel, ConfigDict, Field


class RelatedPartyRef(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None, alias="partyId", description="Identifier of the related party."
    )
    role: str | None = Field(
        None, alias="partyRole", description="Role of the related party."
    )
    href: str | None = Field(None, description="Reference of the related party, could be a party reference or a party "
                                               "role reference.")
    name: str | None = Field(None, description="Name of the related party.")
    referred_type: str | None = Field(
        None, alias="@referredType", description="Indicates the type of the referred object. This attribute is to be "
                                                 "used when the object is representing a reference to an existing "
                                                 "object instead of the of the object itself."
    )
