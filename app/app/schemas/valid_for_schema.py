from pydantic import BaseModel, Field, ConfigDict
import datetime

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ValidFor(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the Valid_for",
    )
    start_date: datetime.datetime | None = Field(
        None,
        alias="startDate",
        description="A date time. The date till the reservation is operating",
    )
