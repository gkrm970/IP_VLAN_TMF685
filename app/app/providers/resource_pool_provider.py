import uuid
from typing import Any, Optional, TypeAlias, Literal
import aiohttp
import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, log, models
from app.core.config import settings
from app.core.exceptions import BadRequestError, InternalServerError

Method: TypeAlias = Literal["GET", "POST", "PATCH"]


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
        self.resource_pool_base_url = settings.API_BASE_URL
        self.resource_pool_api_prefix = settings.API_PREFIX

    async def extract_capacity_amount(self, capacity):
        capacity_amount_remaining = capacity.get("capacity_amount_remaining")
        log.info(f"amount, {capacity_amount_remaining}")
        capacity_amount_from = capacity.get("capacity_amount_from")
        log.info(f"from, {capacity_amount_from}")
        capacity_amount_to = capacity.get("capacity_amount_to")
        resource = capacity.get("resource")
        return capacity_amount_remaining, capacity_amount_from, capacity_amount_to, resource

    async def extract_related_party(self, capacity: schemas.ResourcePool):
        related_party_id = capacity.get("relatedParty").get("party_id")
        return related_party_id

    @staticmethod
    async def generate_unique_vlan(demand_amount, capacity_amount_from, capacity_amount_to, used_vlans):
        log.info(f"demand_amount: {demand_amount}")
        vlans_list = []
        available_vlans = list(range(capacity_amount_from, capacity_amount_to + 1))

        # Filter out used VLANs
        available_vlans = [vlan for vlan in available_vlans if vlan not in used_vlans]

        for vlan in available_vlans:
            vlans_list.append(vlan)
            log.info(f"vlans_list: {vlans_list}")
            if len(vlans_list) == demand_amount:
                break

        return vlans_list
        # for vlan in range(capacity_amount_from, capacity_amount_to + 1):
        #     if vlan not in used_vlans and vlan not in vlans_list:
        #         vlans_list.append(vlan)
        #         log.info(f"vlans_list: {vlans_list}")
        #         if len(vlans_list) == demand_amount:
        #             break
        # return vlans_list

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

    async def get_resource(self, href: str) -> dict[str, Any]:
        response = await self._send_request("GET", href)
        try:
            if response.status_code == 200:
                return response.json()
            else:
                error_message = f"Bad request. Expected status code 200, but received {response.status_code}."
                raise BadRequestError(error_message)
        except Exception as e:
            raise BadRequestError(f"Bad request. Status code: {response.status_code}")

    @staticmethod
    async def _send_patch_request(method: Method, url: str,
                                  request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                log.info("data=%s", request_body)
                response = await client.patch(url, json=request_body)
                tmf_685_patch = response.json()
                log.info("tmf_685_patch_status_code=%s", response.status_code)
                log.info("tmf_685_patch_content_response=%s", tmf_685_patch)

                return tmf_685_patch
        except httpx.HTTPStatusError as e:
            log.info(f"Failed to send PATCH request. HTTP status error: {e}")
            raise e
        except httpx.RequestError as e:
            log.info(f"Failed to send PATCH request. Request error: {e}")
            raise e

    # @staticmethod
    # async def create_resource_reservation_response(db: AsyncSession, used_vlans,
    #                                                demand_amount, related_party_id,
    #                                                resource_inventory_href,
    #                                                resource_inventory_id) -> None | dict | Any:
    #     # try:
    #     print("inside try")
    #         applied_capacity = models.AppliedCapacityAmount(
        #         id=str(uuid.uuid4()),
        #         applied_capacity_amount=demand_amount
        #     )
        #     db.add(applied_capacity)
        #     await db.commit()
        #
        #     models.ReservationResource(
        #         # id=str(uuid.uuid4()),
        #         referred_type=related_party_id,
        #         href=resource_inventory_href,
        #         resource_id=resource_inventory_id
        #     )
        #     await db.commit()
        #     models.Characteristic(
        #         # id=str(uuid.uuid4()),
        #         ipv4_subnet=used_vlans
        #     )
        #     await db.commit()
        #     return True
        # except Exception as e:
        #     raise InternalServerError("An error occurred while creating resource reservation response") from e

    #     demand_amount = reservation_item[0].reservation_resource_capacity.capacity_demand_amount
    #     applied_capacity_amount = {
    #         "appliedCapacityAmount": str(demand_amount),
    #         "resource": []
    #     }
    #     for vlan in used_vlans:
    #         characteristic = {
    #             "8021qVLAN": vlan
    #         }
    #
    #         applied_capacity_amount["resource"].append({
    #             "@referredType": "VLAN",
    #             "href": resource_inventory_href,
    #             "resource_id": resource_inventory_id,
    #             "characteristic": characteristic
    #         })
    #
    #     reservation_response = await create_reservation_response(reservation_item, applied_capacity_amount)
    #     return reservation_response
    #
    # async def patch_resource_pool(self, resource_inventory_href, resource_inventory_id, available_capacity_amount,
    #                               resource_pool_id, reserved_vlans, db):
    #     log.info("available_capacity_amount", available_capacity_amount)
    #     resource_pool_patch_url = f"{self.resource_pool_base_url}/{self.resource_pool_api_prefix}/{resource_pool_id}"
    #
    #     async with aiohttp.ClientSession() as session:
    #         log.info("patch_url=%s", resource_pool_patch_url)
    #
    #         patch_data = {
    #             "@type": "VLAN_ResourcePool",
    #             "capacity": [
    #                 {
    #                     "applicableTimePeriod": {
    #                         "from": "2019-08-24T14:15:22Z"
    #                     },
    #                     "capacityAmount": "100",
    #                     "capacityAmountFrom": "2000",
    #                     "capacityAmountRemaining": str(available_capacity_amount),
    #                     "capacityAmountTo": "2099",
    #                     "place": [
    #                         {
    #                             "name": "AB",
    #                             "type": "region"
    #                         },
    #                         {
    #                             "name": "Viger-1",
    #                             "type": "pod"
    #                         }
    #                     ],
    #                     "rangeInterval": "1",
    #                     "relatedParty": {
    #                         "party_id": "tinaa",
    #                         "name": "CNM Network",
    #                         "role": "tinaaVLANPool"
    #                     },
    #                     "resourceSpecification": [
    #                         {
    #                             "@type": "8021qVLAN_ResourceSpecification",
    #                             "href": "https://api.develop.tinaa.teluslabs.net/plan/inventory"
    #                                     "/resourceCatalogManagement"
    #                                     "/resourceSpecification/99214f4f-6cfc-41a8-9c8e-3b94707ec939",
    #                             "resource_specification_id": "99214f4f-6cfc-41a8-9c8e-3b94707ec939"
    #                         }
    #                     ],
    #                     "resource": [
    #                         {
    #                             "href": resource_inventory_href,
    #                             "id": resource_inventory_id
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "description": "VLAN Resource Pool",
    #             "name": "Some ABC VLAN Pool"
    #         }
    #
    #         async with session.patch(resource_pool_patch_url, json=patch_data) as response:
    #             log.info("response_685=%s", response.json())
    #             if response.status == 200:
    #                 log.info("Resource pool patched successfully")
    #                 return response.json()
    #             else:
    #                 log.error(f"Failed to patch resource pool. Status code: {response.status}")
    #                 raise BadRequestError(f"Failed to patch resource pool. Status code: {response.status}")


resource_pool_provider = ResourcePoolProvider()
