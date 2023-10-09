import datetime

from pydantic import BaseModel, ConfigDict, Field

from app import schemas


class ResourceCapacityDemand(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    resource_capacity_demand_amount: str | None = Field(None, alias="@resourceCapacityDemandAmount",
                                                        description="The amount of the resource capacity demand.  A "
                                                                    "value and units that define the CapacityDemand, "
                                                                    "such as 10000 ea, 10B Instance values are "
                                                                    "mutually exclusive with From and To "
                                                                    "capacityDemandAmounts and range interval.")
    base_type: str | None = Field(None, alias="@baseType",
                                  description="Generic attribute indicating the base class type of"
                                              "the extension class of the current object. Useful only when"
                                              "the class type of the current object is unknown to the "
                                              "implementation.")

    id: str | None = Field(None, description="Identifier of the product offering.")
    schema_location: str | None = Field(None, alias="@schemaLocation", description="the link to the "
                                                                                   "schema that defines the structure "
                                                                                   "of the class type of the"
                                                                                   "current object. ")
    type: str | None = Field(None, alias="@type", description="Class type of the product offering.")
    applicable_time_period: datetime.datetime = Field(default_factory=datetime.datetime.today,
                                                      alias="@applicableTimePeriod", description="The period of time "
                                                                                                 "for which Capacity "
                                                                                                 "or CapacityDemand "
                                                                                                 "applies.")
    place: str | None = Field(None, description="A place, location, or point of attachment.")
    pattern: str | None = Field(None, description="A regular expression to define the pattern for the capacity "
                                                  "demand amount.")
    category: str | None = Field(None, description="Category of the productOffering.")

    # ResourcePool is nesting schema of ResourceCapacityDemand schema
    resource_pool_ref: schemas.ResourcePool | None = Field(None, alias="resourcePool",
                                                           description="Reference of the ResourcePool.")
