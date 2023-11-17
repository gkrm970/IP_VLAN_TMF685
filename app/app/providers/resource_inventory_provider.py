import json
from typing import Any, Optional
from urllib.parse import urljoin
# from .resource_pool_provider import vlan_manager
import httpx

from app import schemas, log
from app.core.config import settings
from ..core.exceptions import InternalServerError


class ResourceInventoryProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX

    async def _send_request(self, method, url: str, request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
        try:

            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=request_body)
                print("response_639_", response)

                return response

        except httpx.HTTPStatusError:
            pass
        except httpx.RequestError:
            pass

    # async def get_resource(self, resource_pool_href: str) -> dict[str, Any]:
    #     response = await self._send_request("GET", urljoin(self.base_url, resource_pool_href))
    #     return response.json()

    # async def _undo_generate_vlan_numbers(self, used_vlans: set[int], generated_vlans: set[int]):
    #     used_vlans -= generated_vlans
    #     return used_vlans

    async def create_resource(self, related_party_id, reservation_item,
                              resource_specification_list, reserved_vlans) -> None | dict | Any:
        # try:
        # print("type=",type(reserved_vlans))
        # vlans_list = list(reserved_vlans)
        # print("type=", type(vlans_list))

        # print("resource_specification_list", reserved_vlans)
        # print("reserved_vlans_11", reserved_vlans)

        reservation_place = reservation_item.reservation_resource_capacity.reservation_place
        # print("reservation_place", reservation_place)

        create_resource_request = {"category": "vlan_Resource", "description": "Vlan",
                                   "name": "pcg-loopback-pc-up-N6_SGi_IMS_v4", "operationalState": "enable",
                                   "resourceCharacteristic": [{"name": related_party_id, "value": vlan} for vlan in
                                                              reserved_vlans], "resourceSpecification": [],
                                   "resourceVersion": "0.0.1", "place": []}
        # print("create_resource_request", create_resource_request)

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

        print("create_resource_request", create_resource_request)

        # response = await self._send_request("POST", urljoin(self.base_url, self.api_prefix),
        # create_resource_request)
        # tmf_639_url = "https://48e8744b-8c35-47d1-bb3d-7e8a35dea502.mock.pstmn.io"
        tmf_639_url = "https://e1abb0a3-48b5-4bf3-924d-970530ad722f.mock.pstmn.io"
        response = await self._send_request("POST", tmf_639_url, create_resource_request)
        if response.status_code == 200:
            return response.json()
        else:
            # await vlan_manager.release_vlan_numbers(reserved_vlans, db)
            raise InternalServerError("TMF639 create resource fails: An error occurred during resource creation.")

        # except Exception as e:
        #     print(f"Error creating resource: {e}")
        #     await vlan_manager.release_vlan_numbers(reserved_vlans, db)
        #     raise InternalServerError("TMF639 create resource fails: An error occurred during resource creation.")


resource_inventory_provider = ResourceInventoryProvider()
