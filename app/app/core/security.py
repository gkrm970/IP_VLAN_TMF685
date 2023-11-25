from typing import Annotated, cast

import httpx
import jose.jwt
import pydantic
from fastapi import Request, Security
from fastapi.openapi.models import OAuthFlowClientCredentials, OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from app import log, schemas
from app.core.config import JWKSet, settings
from app.core.exceptions import InternalServerError, UnauthorizedError


class OAuth2ClientCredentialsBearer(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str | None = None,
        scopes: dict | None = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlows(
            clientCredentials=cast(
                OAuthFlowClientCredentials, {"tokenUrl": token_url, "scopes": scopes}
            )
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        auth_header: str | None = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(auth_header)

        if not auth_header or scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedError(
                    "Not authenticated", headers={"WWW-Authenticate": "Bearer"}
                )

            else:
                return None

        return param


async def _get_jwk_set() -> JWKSet:
    if settings.AUTH_JWK_SET is None:
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(str(settings.AUTH_JWK_SET_URL))

                response.raise_for_status()

                settings.AUTH_JWK_SET = response.json()

        except httpx.RequestError as exc:
            log.error(
                f"An error occurred while getting the JSON Web Key Set "
                f"from '{settings.AUTH_JWK_SET_URL}': {exc}"
            )
            raise

    return settings.AUTH_JWK_SET


_oauth2_scheme = OAuth2ClientCredentialsBearer(token_url=str(settings.AUTH_TOKEN_URL))


async def validate_token_signature(
    token: Annotated[str, Security(_oauth2_scheme)]
) -> schemas.TokenPayload:
    jwk_set = await _get_jwk_set()

    try:
        claims = jose.jwt.decode(token, jwk_set, audience="account")
        payload = schemas.TokenPayload.model_validate(claims)

    except pydantic.ValidationError as exc:
        log.error(f"Unexpected auth token payload format: {exc}")
        raise InternalServerError("Unexpected auth token payload format")

    except jose.JWTError:
        raise UnauthorizedError("Invalid authentication details")

    return payload


class AccessRoleValidator:
    def __init__(self, roles: list[str]) -> None:
        self.roles = roles

    async def __call__(
        self, token: Annotated[schemas.TokenPayload, Security(validate_token_signature)]
    ) -> schemas.TokenPayload:
        client_resource_access = token.resource_access.get(settings.AUTH_CLIENT_ID)

        if client_resource_access is None:
            raise UnauthorizedError(
                f"No permission to access the requested resource, "
                f"missing resource access: '{settings.AUTH_CLIENT_ID}'"
            )

        if not any(role in client_resource_access.roles for role in self.roles):
            raise UnauthorizedError(
                f"Not enough permissions to access the requested resource, "
                f"missing role: one of '{' '.join(self.roles)}'"
            )

        return token


resource_pool_read_access = Security(
    AccessRoleValidator(
        [
            "uinv:tmf685:resourcepool:ro",
            "uinv:tmf685:resourcepool:rw",
        ]
    )
)

resource_pool_read_write_access = Security(
    AccessRoleValidator(
        [
            "uinv:tmf685:resourcepool:rw",
        ]
    )
)

reservation_read_access = Security(
    AccessRoleValidator(["uinv:tmf685:reservation:ro", "uinv:tmf685:reservation:rw"])
)

reservation_read_write_access = Security(
    AccessRoleValidator(["uinv:tmf685:reservation:rw"])
)
