from pydantic import BaseModel, Field, ConfigDict

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class Characteristic(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )
    ipv4_subnet: str | None = Field(
        None,
        alias="ipv4Subnet",
        description="When sub-classing, this defines the super-class",
    )
