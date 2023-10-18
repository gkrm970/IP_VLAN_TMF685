from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class Resource(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )
    referred_type: str | None = Field(
        None,
        alias="@referredType",
        description="When sub-classing, this defines the super-class",
    )
    href: str | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    resource_id: str | None = Field(
        None,
        description="When sub-classing, this defines the super-class",
    )
    characteristic: list[schemas.Characteristic] = Field(
        default_factory=list, description="Array of objects (Note)"
    )
