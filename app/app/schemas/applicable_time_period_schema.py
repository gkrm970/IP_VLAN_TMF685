from pydantic import BaseModel, Field


class ApplicableTimePeriod(BaseModel):
    fromDateTime: str | None = Field(None, alias="from", description="Start of the period.")
    toDateTime: str | None = Field(None, alias="to", description="End of the period.")

