from pydantic import BaseModel, ConfigDict, Field

_NAME_DESCRIPTION = "A string used to give a name to the resource"


class Capacity(BaseModel):
    baseType: str | None = Field(None, alias="@baseType", description="A string. Generic attribute indicating the base "
                                                                      "class type of the extension class of the "
                                                                      "current object. Useful only when the class ")
    schemaLocation: str | None = Field(None, alias="@schemaLocation", description="A string. Generic attribute "
                                                                                  "containing the link to the schema ")
    type: str | None = Field(None, alias="@type",
                             description="A string. Generic attribute containing the name of the "                                                           "resource class type")
    plannedOrActualCapacity: str | None = Field(None,
                                                description="A string. Indicates whether the capacity is planned "                                                            "or actual.")


class CapacityAmount(BaseModel):
    capacityAmount: str | None = Field(None, description="A string. Amount of the capacity amount.")
    capacityAmountFrom: str | None = Field(None, description="A string. Start of the capacity amount.")
    capacityAmountTo: str | None = Field(None, description="A string. End of the capacity amount.")
    rangeInterval: str | None = Field(None, description="A string. Range interval of the capacity amount.")


class AppliedCapacityAmount(BaseModel):
    baseType: str | None = Field(None, alias="@baseType",
                                 description="A string. Generic attribute indicating the base class type of the ")
    schemaLocation: str | None = Field(None, alias="@schemaLocation",
                                       description="A string. Generic attribute containing the link to the ")
    type: str | None = Field(None, alias="@type", description="A string. Generic attribute containing the name of the ")
    appliedDemandAmount: str | None = Field(None,
                                            description="An amount of demand applied to a CapacityAmount. Note that this")


class RelatedPartyRef(BaseModel):
    id: str = Field(None, description="Identifier of the related party")
    href: str | None = Field(None,
                             description="A string. Reference of the related party, could be a party reference or")
    name: str | None = Field(None, description="A string. Name of the related party.")
    role: str | None = Field(None, description="A string. Role of the related party.")
    referredType: str | None = Field(None, description="A string. Type of the related party.")


class PlaceRef(BaseModel):
    type: str | None = Field(None, description="A string. Type of the place.")
    name: str | None = Field(None, description="A string. Name of the place.")
    referredType: str | None = Field(None, alias="@referredType", description="A string. Type of the place.")
    href: str | None = Field(None, description="A string. Reference of the place.")


class GraphicalPlaceRef(BaseModel):
    id: str | None = Field(None, description="Identifier of the graphical place")
    href: str | None = Field(None, description="A string. Reference of the graphical place.")
    referredType: str | None = Field(None, alias="@referredType", description="A string. Type of the graphical place.")


class ResourceAttributesDescription(BaseModel):
    id: int = Field(None, description="Identifier of the resource attributes description")
    href: str | None = Field(None, description="A string. Reference of the resource attributes description.")
    description: str | None = Field(None, description="A string. Description of the resource attributes description.")
    name: str | None = Field(None, description="A string. Name of the resource attributes description.")
    state: str | None = Field(None, description="A string. State of the resource attributes description.")
    place: PlaceRef | None = Field(None, description="A place reference. The place for which the resource attributes ")
    referredType: str | None = Field(None, description="A string. Type of the resource attributes description.")
    resourceCharacteristic: dict | None = Field(None, description="A list of resource characteristics. The resource ")
    relatedParty: RelatedPartyRef | None = Field(None, description="A related party reference. The related party ")


class ApplicableTimePeriod(BaseModel):
    fromToDateTime: str = Field(None, description="A string. Start date of the applicable time period.")
    rangeInterval: str = Field(None, description="A string. End date of the applicable time period.")
    daysOfWeek: str = Field(None, description="A string. Days of the week for which the applicable time period is ")
    validFor: str = Field(None, description="A string. The period of time for which the applicable time period is ")
    baseType: str | None = Field(None, description="A string. Generic attribute indicating the base class type of the ")
    schemaLocation: str | None = Field(None, description="A string. Generic attribute containing the link to the ")
    type: str | None = Field(None, description="A string. Type of the applicable time period.")


class ResourceCollectionRef(BaseModel):
    name: str | None = Field(None, description="Represents a user-friendly identifier of an object")
    href: str | None = Field(None, description="A string. Hyperlink to access the Resource collection.")
    ObjectId: str | None = Field(None, description="A list of consisted Resources")
    referredType: str | None = Field(None, alias="@referredType",
                                     description="A string. Indicates the type of the referred object. This attribute "
                                                 "is to"
                                                 "be used when the object is representing a reference to an existing "
                                                 "object instead of the of the object itself.")


class ResourcePool(BaseModel):
    href: str | None = Field(None, description="A string. Reference of the resource pool.")
    description: str | None = Field(None, description="A string. Description of the resource pool.")
    relatedParty: RelatedPartyRef | None = Field(None, description="A related party reference. The related party ")
    resourceCollection: ResourceCollectionRef | None = Field(None,
                                                             description="A resource collection reference. The resource ")
    baseType: str | None = Field(None, description="A string. Generic attribute indicating the base class type of the ")
    schemaLocation: str | None = Field(None, description="A string. Generic attribute containing the link to the "
                                                         "schema ")
    type: str | None = Field(None, description="A string. Type of the resource pool.")


class ResourceRef(BaseModel):
    id: str = Field(None, description="Identifier of the resource")
    href: str | None = Field(None, description="A string. Reference of the resource.")
    referredType: str | None = Field(None, description="A string. Type of the resource.")
    value: str | None = Field(None, description="A string. Value of the resource.")


class ResourceCapacityDemand(BaseModel):
    id: int = Field(None, description="Identifier of the resource capacity demand")
    resourceCapacityDemandAmount: str = Field(..., description="A string. Amount of the resource capacity "
                                                               "demand.")
    applicableTimePeriod: ApplicableTimePeriod | None = Field(None,
                                                              description="A time period. The time period for which "
                                                                          "the resource"
                                                                          "capacity demand is applicable.")
    place: PlaceRef = Field(None, description="A place reference. The place for which the resource capacity demand "
                                              "is applicable.")
    resourcePool: ResourcePool = Field(None, description="A resource pool reference. The resource pool for which "
                                                         "the resource capacity demand is applicable.")
    type: str | None = Field(None, alias="@type", description="A string. Type of the resource capacity demand.")
    baseType: str | None = Field(None, description="A string. Generic attribute indicating the base class type of"
                                                   "the extension class of the current object. Useful only when "
                                                   "the class type of the current object is unknown to the "
                                                   "implementation.")
    schemaLocation: str | None = Field(None, description="A string. Generic attribute containing the link to the "
                                                         "schema that defines the structure of the class type of the "
                                                         "current object.")
    category: str | None = Field(None, description="A string. The category of resources that is being asked for. E.g."
                                                   ":Regular/ Gold for Logical Resources"
                                                   "Used to indicate reserved resources")
    pattern: str | None = Field(None, description="Used to define a place useful for the resource"
                                                  "Used to indicate reserved resources")
    resource: ResourceRef | None = Field(None, description="Used to define a place useful for the resource")


class AppliedResourceCapacity(BaseModel):
    appliedDemandAmount: str | None = Field(None,
                                            description="An amount of demand applied to a CapacityAmount. Note that "
                                                        "this"
                                                        "is a composite attribute defined by CapacityAmount.")
    resourceRef: dict | None = Field(None, description="A list of resources being referred to in the"
                                                       "appliedResourceCapacity")
    baseType: str | None = Field(None, description="A string. Generic attribute indicating the base class type of the "
                                                   "extension class of the current object. Useful only when the class "
                                                   "type of the current object is unknown to the implementation.")
    schemaLocation: str | None = Field(None,
                                       description="A string. Generic attribute containing the link to the schema that "
                                                   "defines the structure of the class type of the current object.")
    type: str | None = Field(None, description="A string. Generic attribute containing the name of the resource "
                                               "class type")


class ProductOfferingRef(BaseModel):
    id: str = Field(None, description="Identifier of the product offering")
    href: str | None = Field(None, description="A string. Reference of the product offering.")
    name: str | None = Field(None, description="A string. Name of the product offering.")
    referredType: str | None = Field(None, description="A string. Type of the product offering.")
    description: str | None = Field(None, description="A string. Description of the product offering.")


class Value(BaseModel):
    id: str = Field(None, description="Identifier of the resource")
    href: str | None = Field(None, description="A string. Reference of the resource.")
    type: str | None = Field(None, alias="@type", description="A string. Type of the resource.")
    value: str | None = Field(None, description="A string. Value of the resource.")


class CapacitySpecRef(BaseModel):
    referredType: str | None = Field(None, alias="@referredType",
                                     description="A string. Type of the referred object. This attribute is to be used "
                                                 "when the object is representing a reference to an existing object "
                                                 "instead of the of the object itself.")
    href: str | None = Field(None, description="A string. Reference of the capacity spec.")
    id: str | None = Field(None, description="Identifier of the capacity spec.")


class ResourceBase(BaseModel):
    baseType: str = Field(None, description="The base type of the resource.")
    schemaLocation: str = Field(None,
                                description="A link to the schema describing a resource.")
    type: str = Field(None, description="The type of the resource.")
    relatedParty: str = Field(None, description="A related party associated with this resource.")
    href: str = Field(None, description="The URI for the object itself.")
    # description: str = Field(None, description="A narrative text describing the resource.")


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    pass


class Resource(ResourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description=(
            "Identifier of an instance of the resource. Required to be unique within "
            "the resource type. Used in URIs as the identifier for specific instances "
            "of a type."
        ),
    )
