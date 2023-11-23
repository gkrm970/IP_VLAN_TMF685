from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ReservationResource(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    referred_type: str | None = Field(
        None, alias="@referredType", description=_NAME_DESCRIPTION
    )

    characteristic: list[schemas.ReservationCharacteristic] = Field(
        ...,
        default_factory=list,
        description="Configuration features",
    )
    href: str | None = Field(None, description=_NAME_DESCRIPTION)
    resource_id: str | None = Field(None, description=_NAME_DESCRIPTION)
