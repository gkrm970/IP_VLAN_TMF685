from pydantic import BaseModel, ConfigDict, Field


class ChannelRef(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    href: str | None = Field(None, description="")
    id: str | None = Field(None, description="")
    name: str | None = Field(None, description="")
    referred_type: str | None = Field(
        None,
        alias="@referredType",
        description="",
    )
