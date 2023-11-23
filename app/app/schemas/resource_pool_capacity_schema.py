from pydantic import BaseModel, ConfigDict, Field

from app import schemas

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class ResourcePoolCapacityBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    capacity_amount: str | None = Field(
        None, alias="capacityAmount", description=_NAME_DESCRIPTION
    )
    capacity_amount_from: str | None = Field(
        None, alias="capacityAmountFrom", description=_NAME_DESCRIPTION
    )
    capacity_amount_remaining: str | None = Field(
        None, alias="capacityAmountRemaining", description=_NAME_DESCRIPTION
    )
    capacity_amount_to: str | None = Field(
        None, alias="capacityAmountTo", description=_NAME_DESCRIPTION
    )
    range_interval: str | None = Field(
        None, alias="rangeInterval", description=_NAME_DESCRIPTION
    )

    applicable_time_period: schemas.ResourcePoolApplicableTimePeriod | None = Field(
        None,
        alias="applicableTimePeriod",
        description="Configuration features",
    )
    related_party: schemas.ResourcePoolRelatedParty = Field(
        ...,
        alias="relatedParty",
        description="Configuration features",
    )

    place: list[schemas.ResourcePoolPlace] = Field(
        ...,
        default_factory=list,
        description="Configuration features",
    )
    resource_specification: list[schemas.ResourcePoolResourceSpecification] = Field(
        alias="resourceSpecification",
        default_factory=list,
        description="Configuration features",
    )


class ResourcePoolCapacityCreate(ResourcePoolCapacityBase):
    resource_pool_resource: list[schemas.ResourcePoolResource] = Field(
        alias="resource",
        default_factory=list,
        description="Configuration features",
    )


class ResourcePoolCapacityUpdate(ResourcePoolCapacityBase):
    resource_pool_resource: list[schemas.ResourcePoolResource] = Field(
        alias="resource",
        default_factory=list,
        description="Configuration features",
    )


class ResourcePoolCapacity(ResourcePoolCapacityBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type"
        ),
    )
    resource_pool_resource: list[schemas.ResourcePoolResource] = Field(
        alias="resource",
        default_factory=list,
        description="Configuration features",
    )
