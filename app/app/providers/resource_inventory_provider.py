from typing import Any, Literal, TypeAlias, Optional
import httpx
from asgi_correlation_id import correlation_id
from app import log
from app.core.exceptions import BadRequestError
from app.core.config import settings
from ..core.exceptions import InternalServerError

Method: TypeAlias = Literal["GET", "POST"]


class ResourceInventoryProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX

    @staticmethod
    async def _send_request(method: Method, url: str, request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
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

    async def create_resource(self, related_party_id, reservation_item,
                              resource_specification_list, reserved_vlans) -> None | dict | Any:
        try:
            reservation_place = reservation_item.reservation_resource_capacity.reservation_place

            create_resource_request = {"category": "vlan_Resource", "description": "Vlan",
                                       "name": "pcg-loopback-pc-up-N6_SGi_IMS_v4", "operationalState": "enable",
                                       "resourceCharacteristic": [{"name": related_party_id, "value": vlan} for vlan in
                                                                  reserved_vlans], "resourceSpecification": [],
                                       "resourceVersion": "0.0.1", "place": []}

            for place_info in reservation_place:
                create_resource_request["place"].append({
                    "name": place_info.name,
                    "role": place_info.type
                })

            for resource_specification_info in resource_specification_list:
                create_resource_request["resourceSpecification"].append({
                    "href": resource_specification_info.get("href"),
                    "id": resource_specification_info.get("id"),
                    "version": "0.0.1"
                })

            tmf_639_url = f"{self.base_url}/{self.api_prefix}"
            tmf_639_url = "https://e1abb0a3-48b5-4bf3-924d-970530ad722f.mock.pstmn.io"
            response = await self._send_request("POST", tmf_639_url, create_resource_request)
            print(f"tmf_639_url_status_code: {response.status_code}")
            print(f"tmf_639_url_response: {response.json()}")
            if response.status_code == 200:  # 201
                log.info("TMF-639 Created successfully")
                return response.json()
            else:
                raise Exception(f"TMF639 create resource fails: {response.status_code} - {response.text}")
        except Exception as e:
            log.info(f"Error creating resource: {e}")
            raise InternalServerError("TMF639 create resource fails: An error occurred during resource creation.")


resource_inventory_provider = ResourceInventoryProvider()
