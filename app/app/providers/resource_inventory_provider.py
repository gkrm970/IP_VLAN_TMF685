from typing import Any, Literal, Optional, TypeAlias
from urllib.parse import urljoin

import httpx
from asgi_correlation_id import correlation_id
from fastapi import status

from app import log, providers, schemas
from app.core.config import settings
from app.core.exceptions import BadRequestError, InternalServerError

Method: TypeAlias = Literal["GET", "POST", "DELETE"]


class ResourceInventoryProvider:
    def __init__(self):
        self.base_api_url = urljoin(str(settings.RI_BASE_URL), settings.RI_API_PREFIX)
        self.created_resource_data = None

    @staticmethod
    async def _send_request(
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

    async def delete_resource_by_id(self, id: str) -> None:
        response = await self._send_request(
            "DELETE", f"{self.base_api_url}/resource/{id}"
        )

        if response.status_code == status.HTTP_204_NO_CONTENT:
            log.info(f"Deleted resource successfully with ID {id}")
        else:
            log.info(f"Failed to delete resource, status code {response.status_code}")

    async def create_resource(
        self,
        reservation_item: schemas.ReservationItemCreate,
        resource_specification_list,
        reserved_vlans,
    ) -> None | dict | Any:
        try:
            reservation_place = (
                reservation_item.reservation_resource_capacity.reservation_place
            )
            resource_type = reservation_item.reservation_resource_capacity.type
            resource_name = reservation_item.resource_name[0].name
            print("resource_name", resource_name)

            create_resource_request = {
                "category": "vlan_Resource",
                "description": "Vlan",
                "name": resource_name,
                "operationalState": "enable",
                "resourceCharacteristic": [
                    {"name": resource_type, "value": vlan} for vlan in reserved_vlans
                ],
                "resourceSpecification": [],
                "resourceVersion": "0.0.1",
                "place": [],
            }

            for place_info in reservation_place:
                create_resource_request["place"].append(
                    {"name": place_info.name, "role": place_info.type}
                )

            for resource_specification_info in resource_specification_list:
                create_resource_request["resourceSpecification"].append(
                    {
                        "href": resource_specification_info.get("href"),
                        "id": resource_specification_info.get("id"),
                        "version": "0.0.1",
                    }
                )

            log.info("create_resource_request=%s", create_resource_request)

            tmf_639_url = f"{self.base_api_url}/resource"
            response = await self._send_request(
                "POST", tmf_639_url, create_resource_request
            )
            log.info("tmf_639_url_status_code=%s", response.status_code)
            log.info("tmf_639_url_response=%s", response.json())
            if response.status_code == status.HTTP_201_CREATED:
                log.info("TMF-639 Created successfully")
                return response.json()
            else:
                raise Exception(
                    "TMF639 create resource fails: "
                    f"{response.status_code} - {response.text}"
                )
        except Exception as e:
            log.info(f"Error creating resource: {e}")
            raise InternalServerError(
                "TMF639 create resource fails: "
                "An error occurred during resource creation."
            )


resource_inventory_provider = ResourceInventoryProvider()
