import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourcePoolPlace(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str | None = Field(
        None,
        description=_NAME_DESCRIPTION)
    type: str | None = Field(
        None,
        description=_NAME_DESCRIPTION)
