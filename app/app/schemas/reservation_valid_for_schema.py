import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ReservationValidFor(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    start_date: datetime.datetime = Field(
        None, alias="startDate", description=_NAME_DESCRIPTION
    )
