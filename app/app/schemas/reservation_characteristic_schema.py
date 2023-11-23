from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ReservationCharacteristic(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    ipv4_subnet: str | None = Field(
        None, alias="ipv4Subnet", description=_NAME_DESCRIPTION
    )
    ipv6_subnet: str | None = Field(
        None, alias="ipv6Subnet", description=_NAME_DESCRIPTION
    )
    vlan_8021q: str | None = Field(
        None, alias="8021q_vlan", description=_NAME_DESCRIPTION
    )
