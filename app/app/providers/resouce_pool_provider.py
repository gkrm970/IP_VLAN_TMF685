import json
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from app import schemas, log
from app.core.config import settings


async def final_reservation_response(reservation_response):
    final_response = []
    return final_response.append(reservation_response)


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

    async def extract_related_party_role(self, capacity: schemas.ResourcePool):
        related_party_role = capacity.get("relatedParty").get("role")
        return related_party_role

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

        if response is not None:
            try:
                return response.json()
            except json.JSONDecodeError:
                log.error(f"Failed to parse JSON response from {resource_pool_href}")

        return {}  # Return an empty dictionary or handle the error case appropriately

    async def create_resource_reservation_response(self, reservation_item, used_vlans,
                                                   resource_inventory_href,
                                                   resource_inventory_id) -> None | dict | Any:
        log.info(f"in reservation capacity_amount: {reservation_item}")
        # Import the necessary classes and modules
        from datetime import datetime

        # Define a function to convert objects to dictionaries
        def convert_to_dict(obj):
            if isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return {key: convert_to_dict(value) for key, value in obj.__dict__.items() if not callable(value)}
            elif isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return obj

        # Convert the data to a dictionary
        converted_data = convert_to_dict(reservation_item)

        # Print the converted data
        print("converted_data", converted_data)

        log.info(f"type_of reservation_item {type(reservation_item)}")
        demand_amount = reservation_item[0].reservation_resource_capacity.capacity_demand_amount
        print("demand_amount_var", demand_amount)

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

        converted_data.append(applied_capacity_amount)

        print("reservation_item_1", converted_data)
        return reservation_item

        # response_data = [applied_capacity_amount]
        #
        # response_json = json.dumps(response_data, ensure_ascii=False)
        # # applied_capacity_amount["appliedCapacityAmount"] = demand_amount
        # #
        # # reservation_item.append(applied_capacity_amount)
        # print("reservation_item_1", response_json)
        #
        # return response_json


resource_pool_instance = ResourcePoolProvider()
