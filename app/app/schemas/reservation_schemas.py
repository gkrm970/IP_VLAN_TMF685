from typing import List

from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class RelatedParty(BaseModel):
    referredType: str
    href: str
    id: str
    name: str
    role: str


class Place(BaseModel):
    referredType: str
    href: str
    id: str
    name: str


class ApplicableTimePeriod(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    dayOfWeek: str
    fromToDateTime: str
    rangeInterval: str
    validFor: str


class ResourcePool(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    description: str
    href: str
    id: str
    relatedParty: str
    resourceCollection: List[Place]


class ResourceCapacity(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    capacityDemandAmount: str
    resourcePool: ResourcePool
    applicableTimePeriod: ApplicableTimePeriod
    place: Place


class AppliedCapacityAmount(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    appliedDemandAmount: str
    resourceCapacityDemand: ResourceCapacity


class ResourceItem(BaseModel):
    baseType: str = Field(None, description="The base type of the resource.")
    schemaLocation: str = Field(None, description="A link to the schema describing a resource.")
    type: str = Field(None, description="The type of the resource.")
    quantity: int = Field(None, description="The quantity of the resource.")
    subReservationState: str = Field(None, description="The state of the sub-reservation.")
    resourceCapacity: ResourceCapacity = Field(None, description="The capacity of the resource.")
    appliedCapacityAmount: AppliedCapacityAmount = Field(None, description="The applied capacity amount.")


class RequestedPeriod(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    daysOfWeek: str
    fromToDateTime: str
    rangeInterval: str
    validFor: str


class ProductOfferingRef(BaseModel):
    href: str
    id: str
    name: str
    bundledProductOffering: List[str]
    referredType: str


class ReservationBase(BaseModel):
    baseType: str = Field(None, description="The base type of the resource.")
    schemaLocation: str = Field(None,
                                description="A link to the schema describing a resource.")
    type: str = Field(None, description="The type of the resource.")
    relatedParty: str = Field(None, description="A related party associated with this resource.")
    href: str = Field(None, description="The URI for the object itself.")
    valid_for: str = Field(None, description="The period for which the object is valid.")
    # reservationItem: List[ResourceItem] = Field(None, description="The items of the reservation.")
    # channelRef: RelatedParty
    # requestedPeriod: RequestedPeriod
    # productOfferingRef: ProductOfferingRef


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )
