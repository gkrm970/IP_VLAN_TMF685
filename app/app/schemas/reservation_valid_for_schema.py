from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ReservationValidFor(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    start_date: str | None = Field(
        None, alias="startDate", description=_NAME_DESCRIPTION
    )

    # class Config:
    #     # Exclude the 'resource' field from the request body
    #     exclude = {'resource'}


# class ReservationValidForCreate(ReservationValidForBase):
#     pass
#
#
# class ReservationValidForUpdate(ReservationValidForBase):
#     pass
#
#
# class ReservationValidFor(ReservationValidForBase):
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
#     start_date: str | None = Field(None, alias="startDate", description=_NAME_DESCRIPTION)
#
