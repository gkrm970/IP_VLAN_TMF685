from pydantic import BaseModel

from app import schemas


class AppliedCapacityAmount(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    appliedDemandAmount: str
    resourceCapacityDemand: ResourceCapacityDemand
