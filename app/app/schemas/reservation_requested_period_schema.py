import datetime

from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationRequestedPeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    from_: datetime.datetime | None = Field(
        None,
        alias="from",
        description="A date time. The date till the reservation is operating",
    )
