
from pydantic import BaseModel, ConfigDict, Field


_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourcePoolRelatedParty(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    party_id: str = Field(..., description=_NAME_DESCRIPTION)
    name: str = Field(..., description=_NAME_DESCRIPTION)
    role: str = Field(..., description=_NAME_DESCRIPTION)
