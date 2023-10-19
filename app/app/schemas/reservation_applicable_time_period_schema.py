import datetime

from pydantic import BaseModel, Field, ConfigDict
from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the reservation"


class ReservationApplicableTimePeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(
        None,
        description="Unique identifier of the feature",
    )
    is_from: datetime.datetime | None = Field(
        None,
        alias="from",
        description="When sub-classing, this defines the super-class",
    )