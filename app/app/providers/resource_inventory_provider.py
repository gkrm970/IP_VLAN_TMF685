import json
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from app import schemas, log
from app.core.config import settings


class ResourceInventoryProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX

    async def _send_request(self, method, url: str, request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
        try:

            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=request_body)
                response_639 = response.json()

                return response_639

        except httpx.HTTPStatusError:
            pass
        except httpx.RequestError:
            pass

    async def get_resource(self, resource_pool_href: str) -> dict[str, Any]:
        response = await self._send_request("GET", urljoin(self.base_url, resource_pool_href))
        return response.json()

    async def create_resource(self, related_party_id, applied_capacity_amount) -> None | dict | Any:

        create_resource_request = {
            "category": "ipv4Subnet_Resource",
            "description": "ipv4Subnet",
            "name": "pcg-loopback-pc-up-N6_SGi_IMS_v4",
            "operationalState": "enable",
            "place": [
                {
                    "name": "Montreal",
                    "role": "geographicRegion"
                },
                {
                    "name": "Viger_POD 1",
                    "role": "podId"
                }
            ],
            "resourceCharacteristic": [{"name": related_party_id, "value": vlan} for vlan in applied_capacity_amount],
            "resourceSpecification": {
                "href": "https://api.develop.tinaa.teluslabs.net/plan/inventory/resourceCatalogManagement/v1/resourceSpecification/def69b28-f380-43a2-9064-18585ffbc613",
                "id": "def69b28-f380-43a2-9064-18585ffbc613",
                "version": "0.0.1"
            },
            "resourceVersion": "0.0.1"
        }

        # response = await self._send_request("POST", urljoin(self.base_url, self.api_prefix), create_resource_request)
        tmf_639_url = "https://48e8744b-8c35-47d1-bb3d-7e8a35dea502.mock.pstmn.io"
        response = await self._send_request("POST", tmf_639_url, create_resource_request)

        return response


resource_inventory_provider = ResourceInventoryProvider()
