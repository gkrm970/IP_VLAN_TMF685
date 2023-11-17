from typing import Any, Optional
import aiohttp
import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app import schemas, log, models
from app.core.config import settings
from app.core.exceptions import NotFoundError, InternalServerError


# class VLANPoolManager:
#     async def initialize_vlan_pool(self, db):
#         try:
#             for vlan_number in range(1, 4096):
#                 vlan_allocation = models.VlanAllocation(vlan_number=vlan_number)
#                 db.add(vlan_allocation)
#             await db.commit()
#         except IntegrityError:
#             await db.rollback()
#
#     async def reserve_vlan_numbers(self, demand_amount, db):
#         try:
#             vlan_numbers = []
#             offset = 0
#             for _ in range(demand_amount):
#                 result = await db.execute(
#                     select(models.VlanAllocation).filter(models.VlanAllocation.is_reserved == False)
#                     .order_by(models.VlanAllocation.vlan_number).offset(offset)
#                     .limit(1).with_for_update()
#                 )
#                 vlan_allocation = result.scalars().first()
#                 if vlan_allocation:
#                     vlan_allocation.is_reserved = True
#                     vlan_numbers.append(vlan_allocation.vlan_number)
#                     offset += 1
#                     print("vlan_numbers", vlan_numbers)
#                 else:
#                     raise NotFoundError("No available VLANs in the pool.")
#             await db.commit()
#             return vlan_numbers
#         except Exception as e:
#             await db.rollback()
#             raise e
#
#     async def release_vlan_numbers(self, vlan_numbers, db):
#         # session = self.Session()
#         try:
#             offset = 0
#             for vlan_number in vlan_numbers:
#                 result = await db.execute(
#                     select(models.VlanAllocation).filter(models.VlanAllocation.is_reserved == True)
#                     .order_by(models.VlanAllocation.vlan_number).offset(offset)
#                     .limit(1).with_for_update()
#                 )
#                 vlan_allocation = result.scalars().first()
#                 print("vlan_allocation", vlan_allocation.vlan_number)
#                 if vlan_allocation:
#                     vlan_allocation.is_reserved = False
#                     offset += 1
#                 else:
#                     raise Exception(f"VLAN {vlan_number} is not reserved.")
#             await db.commit()
#         except Exception as e:
#             await db.rollback()
#             raise e


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
        capacity_amount_remaining = capacity.get("capacity_amount_remaining")
        print("amount", capacity_amount_remaining)
        capacity_amount_from = capacity.get("capacity_amount_from")
        print("from", capacity_amount_from)
        capacity_amount_to = capacity.get("capacity_amount_to")
        resource = capacity.get("resource")
        return capacity_amount_remaining, capacity_amount_from, capacity_amount_to, resource

    async def extract_related_party(self, capacity: schemas.ResourcePool):
        related_party_id = capacity.get("relatedParty").get("party_id")
        return related_party_id

    async def generate_unique_vlan(self, capacity_amount):
        print("capacity_amount_", capacity_amount)
        vlans_list = []
        for vlan in range(1, capacity_amount + 1):
            if vlan not in vlans_list:
                vlans_list.append(vlan)
                print("vlans_list_", vlans_list)
        return vlans_list
        # return None

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

    async def _send_patch_request(self, url: str, request_body: Optional[dict[str, Any]] = None) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                log.info("data=%s", request_body)
                response = await client.patch(url, json=request_body)
                # tmf_685_patch = response.content.decode('utf-8')
                tmf_685_patch = response.json()
                log.info("tmf_685_patch_status_code=%s", response.status_code)
                log.info("tmf_685_patch_content_response=%s", tmf_685_patch)

                return tmf_685_patch
        except httpx.HTTPStatusError as e:
            print(f"Failed to send PATCH request. HTTP status error: {e}")
            raise e
        except httpx.RequestError as e:
            print(f"Failed to send PATCH request. Request error: {e}")
            raise e

    # async def get_resource(self, resource_pool_href: str) -> dict[str, Any]:
    #     print("href",resource_pool_href)
    #     response = await self._send_request("GET", resource_pool_href)
    #     # print("resource_pool_response", response.json())
    #     # response = await self._send_request("GET", urljoin(self.base_url, resource_pool_href))
    #     return response.json()
    async def get_resource(self, resource_pool_href):
        async with httpx.AsyncClient() as client:
            response = await client.get(resource_pool_href, timeout=30)
            response.raise_for_status()
            return response.json()
    # else:
    #             print(f"Error fetching resource pool: {response.status_code}")
            # return response.json() if response.status_code == 200 else None

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

    # async def _undo_generate_vlan_numbers(self, used_vlans: set[int], generated_vlans: set[int]):
    #     used_vlans -= generated_vlans
    #
    # async def _undo_create_resource(self, related_party_id: str, reserved_vlans: set[int]):
    #     await self.resource_inventory_provider.undo_create_resource(related_party_id, reserved_vlans)

    async def patch_resource_pool(self, resource_inventory_href, resource_inventory_id, available_capacity_amount,
                                  resource_pool_id, reserved_vlans, db):
        print("available_capacity_amount", available_capacity_amount)

        # try:
        tmf685_patch_url = "http://127.0.0.1:8000/resourcePoolManagement/v1/resourcePool"

        async with aiohttp.ClientSession() as session:
            patch_url = f"{tmf685_patch_url}/{resource_pool_id}"
            log.info("patch_url=%s", patch_url)

            patch_data = {
                "@type": "VLAN_ResourcePool",
                "capacity": [
                    {
                        "applicableTimePeriod": {
                            "from": "2019-08-24T14:15:22Z"
                        },
                        "capacityAmount": "100",
                        "capacityAmountFrom": "2000",
                        "capacityAmountRemaining": str(available_capacity_amount),
                        "capacityAmountTo": "2099",
                        "place": [
                            {
                                "name": "AB",
                                "type": "region"
                            },
                            {
                                "name": "Viger-1",
                                "type": "pod"
                            }
                        ],
                        "rangeInterval": "1",
                        "relatedParty": {
                            "party_id": "tinaa",
                            "name": "CNM Network",
                            "role": "tinaaVLANPool"
                        },
                        "resourceSpecification": [
                            {
                                "@type": "8021qVLAN_ResourceSpecification",
                                "href": "https://api.develop.tinaa.teluslabs.net/plan/inventory"
                                        "/resourceCatalogManagement"
                                        "/resourceSpecification/99214f4f-6cfc-41a8-9c8e-3b94707ec939",
                                "resource_specification_id": "99214f4f-6cfc-41a8-9c8e-3b94707ec939"
                            }
                        ],
                        "resource": [
                            {
                                "href": resource_inventory_href,
                                "id": resource_inventory_id
                            }
                        ]
                    }
                ],
                "description": "VLAN Resource Pool",
                "name": "Some ABC VLAN Pool"
            }

            print("patch_data", patch_data)

            # resource_data = {
            #     "resource": [
            #         {
            #             "href": resource_inventory_href,
            #             "id": resource_inventory_id
            #         }
            #     ]
            # }
            # patch_data.update(resource_data)

            async with session.patch(patch_url, json=patch_data) as response:
                # response_text = await response.text()
                log.info("response_685=%s", response.json())
                if response.status == 201:
                    log.info("Resource pool patched successfully")
                    return response.json()
                else:
                    log.error(f"Failed to patch resource pool. Status code: {response.status}")
                    # await vlan_manager.release_vlan_numbers(reserved_vlans, db)
                    # url = f'{self.base_url}/{self.api_prefix}/{resource_inventory_id}'
                    # response = await self._send_request("DELETE", url)
                    # if response.status_code == 204:
                    #     raise InternalServerError(
                    #         "TMF685 patch resource pool fails: An error occurred during resource pool updation.")

        # for resource_info in reservation_place:
        #     create_resource_request["place"].append({
        #         "name": place_info.name,
        #         "role": place_info.type
        #     })

        #     {
        #
        #     "capacityAmountRemaining": "new_value",  # Replace with the actual new value
        #     # Add other fields to update as needed
        # }

        # patch_data = {
        #     "capacityAmountRemaining": available_capacity_amount,
        #     # Add other fields that you want to update
        # }

        # patch_url = "https://f26c51a2-3e80-496e-884f-e600ff462378.mock.pstmn.io"
        # response = await self._send_patch_request(patch_url, patch_data)
        # log.info(f'status_code', response.status_code)
        # if response.status_code == 200:
        #     log.info(f'685_patch_response_12300, {response}')
        #     return response
        # else:
        #     log.error("Failed to update resource pool")
        #     raise HTTPException(status_code=response.status_code, detail="Failed to update resource pool")

        # return response
    # except Exception as e:
    #     # Undo operations in case of failure
    #     await self._undo_generate_vlan_numbers(used_vlans, reserved_vlans)
    #     await self._undo_create_resource("tinaa", reserved_vlans)
    #     raise e

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
# vlan_manager = VLANPoolManager()
