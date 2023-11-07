from pydantic import BaseModel, ConfigDict, Field


class ExternalPartyCharacteristics(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    ipam_description: str | None = Field(None,
                                         alias="IPAM Description ",
                                         description="Name of the related entity")
    ipam_details: str | None = Field(None,
                                     alias="IPAM Details",
                                     description="Role played by the related party")
