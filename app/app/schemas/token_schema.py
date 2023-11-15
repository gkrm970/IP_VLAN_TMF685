from pydantic import UUID4, BaseModel


class TokenAccessDetails(BaseModel):
    roles: list[str]


class TokenPayload(BaseModel):
    exp: int
    iat: int
    iss: str
    aud: list[str]
    sub: UUID4
    realm_access: TokenAccessDetails
    resource_access: dict[str, TokenAccessDetails]
    scope: str
