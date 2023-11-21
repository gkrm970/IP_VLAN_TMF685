import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class AppliedCapacityAmount(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    applied_capacity_amount: str | None = Field(None, alias="appliedCapacityAmount", description=_NAME_DESCRIPTION)

    reservation_resource: list[schemas.ReservationResource] = Field(
        ...,
        alias="resource",
        default_factory=list,
        description="Configuration features",
    )

#     # class Config:
#     #     # Exclude the 'resource' field from the request body
#     #     exclude = {'resource'}
#
#
# class AppliedCapacityAmountCreate(AppliedCapacityAmountBase):
#     pass
#
#
# class AppliedCapacityAmountUpdate(AppliedCapacityAmountBase):
#     pass
#
#
# class AppliedCapacityAmount(AppliedCapacityAmountBase):
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
#     applied_capacity_amount: str | None = Field(None, alias="appliedCapacityAmount", description=_NAME_DESCRIPTION)
#
#     reservation_resource: list[schemas.ReservationResource] = Field(
#         ...,
#         alias="resource",
#         default_factory=list,
#         description="Configuration features",
#     )
