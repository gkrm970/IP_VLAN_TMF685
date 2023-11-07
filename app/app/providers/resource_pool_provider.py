from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from app import schemas, models, log
from app.core.config import settings
from app.crud import reservation


class ResourcePoolProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX

    async def extract_capacity_amount(self, capacity):
        capacity_amount = capacity.get("capacityAmount")
        return capacity_amount

    async def extract_related_party(self, capacity: schemas.ResourcePool):
        related_party_id = capacity.get("relatedParty").get("id")
        return related_party_id

    async def generate_unique_vlan(self, capacity_amount, used_vlans):
        for vlan in range(1, capacity_amount + 1):
            if vlan not in used_vlans:
                used_vlans.add(vlan)
                return vlan
        return None

    async def _send_request(self, method, url: str, request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=request_body)
                response.raise_for_status()
                return response

        except httpx.HTTPStatusError:
            pass
        except httpx.RequestError:
            pass

    async def get_resource(self, resource_pool_href: str) -> dict[str, Any]:
        response = await self._send_request("GET", resource_pool_href)
        # response = await self._send_request("GET", urljoin(self.base_url, resource_pool_href))
        return response.json()

    async def create_resource_reservation_response(self, reservation_item, used_vlans,
                                                   resource_inventory_href,
                                                   resource_inventory_id) -> None | dict | Any:
        log.info(f"in reservation capacity_amount: {reservation_item}")
        log.info(f"type_of reservation_item {type(reservation_item)}")
        # demand_amount = reservation_item.reservation_resource_capacity.capacity_demand_amount
        demand_amount = "10"

        applied_capacity_amount = {
            "appliedCapacityAmount": str(demand_amount),
            "resource": []
        }
        for vlan in used_vlans:
            characteristic = {
                "8021qVLAN": vlan
            }

            applied_capacity_amount["resource"].append({
                "@referredType": "VLAN",
                "href": resource_inventory_href,
                "resource_id": resource_inventory_id,
                "characteristic": characteristic
            })
        applied_capacity_amount["appliedCapacityAmount"] = demand_amount

        final_res = reservation_item.append(applied_capacity_amount)
        print("final_res", final_res)

        return final_res


resource_pool_provider = ResourcePoolProvider()
