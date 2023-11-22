from typing import Any, Literal, Optional, TypeAlias

import httpx
from asgi_correlation_id import correlation_id

from app import log
from app.core.config import settings
from app.core.exceptions import BadRequestError

from ..core.exceptions import InternalServerError

Method: TypeAlias = Literal["GET", "POST"]


class ResourceInventoryProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX
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
                    headers={"X-Request-ID": correlation_id.get() or ""},
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

    async def get_resource(self, href: str) -> dict[str, Any]:
        response = await self._send_request("GET", href)
        return response.json()

    async def delete_request(self, resource_inventory_id: str) -> httpx.Response:
        url = f"{self.base_url}/{self.api_prefix}/{resource_inventory_id}"
        try:
            async with httpx.AsyncClient() as client:
                log.debug(f"Sending DELETE request to URL '{url}'")
                response = await client.delete(
                    url,
                    headers={"X-Request-ID": correlation_id.get() or ""},
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

    async def create_resource(
        self, reservation_item, resource_specification_list, reserved_vlans
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

            tmf_639_url = f"{self.base_url}/{self.api_prefix}"
            tmf_639_url = "https://b70b1998-f6bd-4273-a9cf-681b43041018.mock.pstmn.io"
            response = await self._send_request(
                "POST", tmf_639_url, create_resource_request
            )
            log.info("tmf_639_url_status_code=%s", response.status_code)
            log.info("tmf_639_url_response=%s", response.json())

            # resource_inventory_id = "http://ResourcePool/HF5R653R37R",
            # resource_inventory_href = "sts65ett7lk56lko89da7t"

            if response.status_code == 201:  # 201
                log.info("TMF-639 Created successfully")
                # self.created_resource_data = {
                #     "resource_inventory_href": resource_inventory_href,
                #     "resource_inventory_id": resource_inventory_id,
                #     "resource_type": resource_type
                # }
                #
                # return self.created_resource_data, response.json()
                return response.json()
            else:
                raise Exception(
                    f"TMF639 create resource fails: {response.status_code} - {response.text}"
                )
        except Exception as e:
            log.info(f"Error creating resource: {e}")
            raise InternalServerError(
                "TMF639 create resource fails: An error occurred during resource creation."
            )


resource_inventory_provider = ResourceInventoryProvider()
