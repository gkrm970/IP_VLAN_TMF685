import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ReservationCharacteristic(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    ipv4_subnet: str | None = Field(None, alias="ipv4Subnet", description=_NAME_DESCRIPTION)
    ipv6_subnet: str | None = Field(None, alias="ipv6Subnet", description=_NAME_DESCRIPTION)
    vlan_8021q: str | None = Field(None, alias="8021q_vlan", description=_NAME_DESCRIPTION)


    # class Config:
    #     # Exclude the 'resource' field from the request body
    #     exclude = {'resource'}


# class ReservationCharacteristicCreate(ReservationCharacteristicBase):
#     pass
#
#
# class ReservationCharacteristicUpdate(ReservationCharacteristicBase):
#     pass
#
#
# class ReservationCharacteristic(ReservationCharacteristicBase):
#     model_config = ConfigDict(from_attributes=True, populate_by_name=True)
#
#     id: str = Field(
#         ...,
#         description=(
#             "Identifier of an instance of the resource. Required to be unique within "
#             "the resource type. Used in URIs as the identifier for specific instances "
#             "of a type"
#         ),
#     )
#
#     ipv4_subnet: str | None = Field(None, alias="ipv4Subnet", description=_NAME_DESCRIPTION)
#
