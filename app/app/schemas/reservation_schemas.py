from typing import List

from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class RelatedParty(BaseModel):
    party_id: str | None = Field(None, alias="id", description="Identifier of the related party.")
    role: str | None = Field(None, description="Role of the related party.")


class Place(BaseModel):
    id: str | None = Field(None, description="Identifier of the place.")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")
    name: str | None = Field(None, description=_NAME_DESCRIPTION)


class ApplicableTimePeriod(BaseModel):
    fromDateTime: str | None = Field(None, alias="from", description="Start of the period.")
    toDateTime: str | None = Field(None, alias="to", description="End of the period.")


class Resource(BaseModel):
    id: str | None = Field(None, description="Identifier of the resource.")
    href: str | None = Field(None, description="The URI for the object itself.")
    value: str | None = Field(None, description="The value of the resource.")
    referred_type: str | None = Field(None, alias="@referredType", description="The actual type of the target instance.")


class ResourcePool(BaseModel):
    id: str | None = Field(None, description="Identifier of the resource pool.")
    href: str | None = Field(None, description="The URI for the object itself.")
    resource: Resource | None = Field(None, description="A resource is an identifiable physical or logical resource.")


class ResourceCapacityDemand(BaseModel):
    resourceCapacityDemandAmount: str | None = Field(None, description="The amount of the resource capacity demand.")
    applicableTimePeriod: ApplicableTimePeriod | None = Field(None,
                                                              description="The period for which the object is valid.")
    place: Place | None = Field(None, description="A place is a spatial area defined by a set of coordinates.")
    resourcePool: ResourcePool | None = Field(None, description="A resource pool is a collection of resources.")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")


class AppliedCapacityAmount(BaseModel):
    baseType: str
    schemaLocation: str
    type: str
    appliedDemandAmount: str
    resourceCapacityDemand: ResourceCapacityDemand


class ResourceReservationItem(BaseModel):
    quantity: str
    resourceCapacityDemand: list[ResourceCapacityDemand] | None = Field(None,
                                                                        description="The resource capacity demand.")


class RequestedPeriod(BaseModel):
    startDate: str | None = Field(None, description="Start date of the requested period.")
    endDate: str | None = Field(None, description="End date of the requested period.")


class ProductOfferingRef(BaseModel):
    href: str | None = Field(None, description="Reference of the product offering.")
    id: str | None = Field(None, description="Identifier of the product offering.")
    description: str | None = Field(None, description="Description of the product offering.")
    schema_location: str | None = Field(None, alias="@schemaLocation",
                                        description="A link to the schema describing a resource.")
    type: str | None = Field(None, alias="@type", description="The type of the resource.")


class ReservationBase(BaseModel):
    schema_location: str = Field(None, alias="@schemaLocation",
                                 description="A link to the schema describing a resource.")
    type: str = Field(None, alias="@type", description="The type of the resource.")
    href: str = Field(None, description="The URI for the object itself.")
    reservation_state: str = Field(None, description="The state of the reservation.")
    valid_for: str = Field(None, description="The period for which the object is valid.")
    base_type: str = Field(None, alias="@baseType", description="The base type of the resource.")
    description: str = Field(None, description="Description of the reservation.")
    related_party: RelatedParty = Field(None, description="A related party associated with this resource.")
    product_offering: ProductOfferingRef = Field(None,
                                                 description="A product offering represents entities that are "
                                                             "orderable from the provider of the catalog, "
                                                             "this resource includes pricing information.")

    # resourceReservationItem: ResourceReservationItem | None = Field(None, description="The items of the reservation.")
    # requestPeriod: RequestedPeriod | None = Field(None, description="The requested period.")


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
    href: str = Field(..., description="The URI for the object itself.")
