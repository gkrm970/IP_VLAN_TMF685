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

    async def create_resource(self, related_party_id, applied_capacity_amount, reservation_item,
                              resource_specification_list) -> None | dict | Any:
        print("resource_specification_list", resource_specification_list)
        reservation_place = reservation_item.reservation_resource_capacity.reservation_place
        # print("reservation_place", reservation_place)

        create_resource_request = {"category": "ipv4Subnet_Resource", "description": "ipv4Subnet",
                                   "name": "pcg-loopback-pc-up-N6_SGi_IMS_v4", "operationalState": "enable",
                                   "resourceCharacteristic": [{"name": related_party_id, "value": vlan} for vlan in
                                                              applied_capacity_amount], "resourceSpecification": [],
                                   "resourceVersion": "0.0.1", "place": []}

        # "resourceSpecification": {
        #     "href": "https://api.develop.tinaa.teluslabs.net/plan/inventory/resourceCatalogManagement/v1"
        #             "/resourceSpecification"
        #             "/def69b28-f380-43a2-9064-18585ffbc613",
        #     "id": "def69b28-f380-43a2-9064-18585ffbc613",
        #     "version": "0.0.1"
        # },

        for place_info in reservation_place:
            create_resource_request["place"].append({
                "name": place_info.name,
                "role": place_info.type
            })

        for resource_specification_info in resource_specification_list:
            print("resource_specification_info", resource_specification_info)
            create_resource_request["resourceSpecification"].append({
                "href": resource_specification_info.get("href"),
                "id": resource_specification_info.get("id"),
                "version": "0.0.1"
            })

        print("create_resource_request_1", create_resource_request)

        # response = await self._send_request("POST", urljoin(self.base_url, self.api_prefix), create_resource_request)
        tmf_639_url = "https://48e8744b-8c35-47d1-bb3d-7e8a35dea502.mock.pstmn.io"
        response = await self._send_request("POST", tmf_639_url, create_resource_request)

        return response


resource_inventory_provider = ResourceInventoryProvider()
