from typing import TypeAlias, Literal, Optional, Any
from asgi_correlation_id import correlation_id

from app import log, providers
import httpx

from app.core.exceptions import BadRequestError

Method: TypeAlias = Literal["GET"]


class ResourceCatalogProvider:
    @staticmethod
    async def send_request(
        method: Method, url: str, request_body: Optional[dict[str, Any]] = None
    ) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                log.debug(f"Sending request to URL '{url}' with method '{method}'")
                response = await client.request(
                    method,
                    url,
                    json=request_body,
                    headers={
                        "Authorization": (
                            f"Bearer {await providers.tinaa_auth.get_access_token()}"
                        ),
                        "X-Request-ID": correlation_id.get() or "",
                    },
                )
                log.debug(f"Response status code: {response.status_code}")

                response.raise_for_status()
                return response

        except httpx.HTTPStatusError as exc:
            client_error_class = 4

            if exc.response.status_code // 100 == client_error_class:
                log.info(exc)
                raise BadRequestError(str(exc))

            log.error(exc)
            raise

        except httpx.RequestError as exc:
            log.error(exc)
            raise


resource_catalog_provider = ResourceCatalogProvider()
