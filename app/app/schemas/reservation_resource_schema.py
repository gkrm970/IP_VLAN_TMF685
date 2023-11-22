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
    # name: str | None = Field(None, description=_NAME_DESCRIPTION)

    # class Config:
    #     # Exclude the 'resource' field from the request body
    #     exclude = {'resource'}


# class ReservationResourceCreate(ReservationResourceBase):
#     pass
#
#
# class ReservationResourceUpdate(ReservationResourceBase):
#     pass
#
#
# class ReservationResource(ReservationResourceBase):
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
#     referred_type: str | None = Field(None, alias="@referredType", description=_NAME_DESCRIPTION)
#
#     characteristic: list[schemas.ReservationCharacteristic] = Field(
#         ...,
#         default_factory=list,
#         description="Configuration features",
#     )
#     href: str | None = Field(None, description=_NAME_DESCRIPTION)
#     resource_id: str | None = Field(None, description=_NAME_DESCRIPTION)
#
