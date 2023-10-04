from pydantic import BaseModel, ConfigDict, Field


class RelatedPartyRef(BaseModel):
    party_id: str | None = Field(None, alias="id", description="Identifier of the related party.")
    role: str | None = Field(None, description="Role of the related party.")
    href: str | None = Field(None, description="Reference of the related party.")
    name: str | None = Field(None, description="Name of the related party.")
    referred_type: str | None = Field(None, description="Type of the related party.")

