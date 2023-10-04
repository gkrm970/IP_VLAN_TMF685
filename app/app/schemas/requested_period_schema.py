from pydantic import BaseModel, Field


class RequestedPeriod(BaseModel):
    startDate: str | None = Field(None, description="Start date of the requested period.")
    endDate: str | None = Field(None, description="End date of the requested period.")
