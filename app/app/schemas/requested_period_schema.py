import datetime

from pydantic import BaseModel, ConfigDict, Field


class RequestedPeriod(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: str | None = Field(None, description="Identifier of the requested period.")
    base_type: str | None = Field(None, alias="@baseType", description="The base type of the resource.")
    schema_location: str | None = Field(None, alias="@schemaLocation", description=" ")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")
    days_of_week: str | None = Field(None, alias="daysOfWeek", description="Days of the week.")
    from_to_date_time: datetime.date = Field(
        default_factory=datetime.date.today, alias="fromToDateTime", description="The period for which the object is valid.")
    range_interval: str | None = Field(None, alias="rangeInterval", description="Range interval.")
    valid_for: datetime.date = Field(default_factory=datetime.date.today, description="The period for which the "
                                                                                      "object is valid.")
