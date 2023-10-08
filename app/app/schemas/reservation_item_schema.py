from pydantic import BaseModel, ConfigDict, Field


class ReservationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str | None = Field(None, description="Identifier of the channel.")
    quantity: int | None = Field(None, description="Represents the number of reservationItems that make up the "
                                                   "reservation.")
    sub_reservation_state: str | None = Field(None, alias="@subReservationState", description="The life cycle state "
                                                                                              "of each reservation "
                                                                                             "item.")
    applied_capacity_amount: str | None = Field(None, alias="@appliedCapacityAmount",
                                                description="The amount of capacityDemand to applied to a "
                                                            "CapacityAmount.")
    base_type: str | None = Field(None, alias="@baseType", description="The (class) type of the resource.", )
    schema_location: str | None = Field(None, alias="@schemaLocation", description="Link to the schema describing ")
    type: str | None = Field(None, alias="@type", description="The (class) type of the resource.", )
