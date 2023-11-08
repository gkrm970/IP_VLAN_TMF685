import json
import re
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from app import schemas, log
from app.core.config import settings


async def final_reservation_response(reservation_response):
    final_response = []
    return final_response.append(reservation_response)


async def create_reservation_response(reservation_item, applied_capacity_amount):
    reservation_list = []
    for item in reservation_item:
        item_data = {
            "reservationItem": [
                {
                    "appliedCapacityAmount": applied_capacity_amount,
                    "quantity": item.quantity,
                    "resourceCapacity": {
                        "@type": item.reservation_resource_capacity.type,
                        "applicableTimePeriod": {
                            "from": item.reservation_resource_capacity.reservation_applicable_time_period.from_.isoformat(),
                        },
                        "place": [
                            {
                                "name": place.name,
                                "type": place.type
                            } for place in item.reservation_resource_capacity.reservation_place],
                        "capacityDemandAmount": item.reservation_resource_capacity.capacity_demand_amount,
                        "resourcePool": {
                            "href": item.reservation_resource_capacity.resource_pool.href,
                            "id": item.reservation_resource_capacity.resource_pool.pool_id,
                        }
                    }
                }
            ]
        }
        reservation_list.append(item_data)
        return reservation_list


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
        # print("resource_pool_response", response.json())
        # response = await self._send_request("GET", urljoin(self.base_url, resource_pool_href))
        return response.json()

    async def create_resource_reservation_response(self, reservation_item, used_vlans,
                                                   resource_inventory_href,
                                                   resource_inventory_id) -> None | dict | Any:

        demand_amount = reservation_item[0].reservation_resource_capacity.capacity_demand_amount
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

        reservation_response = await create_reservation_response(reservation_item, applied_capacity_amount)
        return reservation_response

        # data_list = []
        #
        # for item in reservation_item:
        #     item_data = {
        #         "reservationItem": [
        #             {
        #                 "appliedCapacityAmount": applied_capacity_amount,
        #                 "quantity": item.quantity,
        #                 "resourceCapacity": {
        #                     "@type": item.reservation_resource_capacity.type,
        #                     "applicableTimePeriod": {
        #                         "from": item.reservation_resource_capacity.reservation_applicable_time_period.from_.isoformat(),
        #                     },
        #                     "place": [
        #                         {
        #                             "name": place.name,
        #                             "type": place.type
        #                         } for place in item.reservation_resource_capacity.reservation_place],
        #                     "capacityDemandAmount": item.reservation_resource_capacity.capacity_demand_amount,
        #                     "resourcePool": {
        #                         "href": item.reservation_resource_capacity.resource_pool.href,
        #                         "id": item.reservation_resource_capacity.resource_pool.pool_id,
        #                     }
        #                 }
        #             }
        #         ]
        #     }
        #     data_list.append(item_data)
        #
        # print("reservation_item_1", data_list)
        # return data_list


resource_pool_provider = ResourcePoolProvider()
