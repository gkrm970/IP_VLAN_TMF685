from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import providers, schemas, log
from app.api import deps
from app.api.deps import get_db_session
from app.core.exceptions import InternalServerError
from app.providers.resource_pool_provider import final_reservation_response


class ResourceReservationManager:
    def __init__(self):
        self.resource_inventory_provider = providers.resource_inventory_provider
        self.resource_pool_provider = providers.resource_pool_provider
        # self.vlan_manager = providers.vlan_manager

    async def _reserve_tinaa_resources(self, demand_amount: int, capacity_amount_remaining: int, used_vlans: set[int],
                                       resource):
        # print("capacity_amount_remaining", demand_amount)
        reserved_vlans = []
        if demand_amount <= capacity_amount_remaining:
            available_capacity_amount = capacity_amount_remaining - demand_amount
            print("resource!=", resource)
            if not resource:
                print("inside")
                # for _ in range(demand_amount):
                unique_vlan = \
                    await self.resource_pool_provider.generate_unique_vlan(demand_amount)
                print("unique_vlan", unique_vlan)
                # if unique_vlan is not None:
                #     reserved_vlans.append(unique_vlan)
                #     print("reserved_vlans", reserved_vlans)
                return unique_vlan
        else:
            print("Not enough resources available to reserve VLANs.")
            raise InternalServerError("Not enough resources available to reserve VLANs.")

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(self, reservation_create: schemas.ReservationCreate, db):
        used_vlans = set()
        reservation_responses = []
        for reservation_item in reservation_create.reservation_item:
            resource_pool_href = reservation_item.reservation_resource_capacity.resource_pool.href
            print("resource_pool_href", resource_pool_href)
            resource_pool_id = reservation_item.reservation_resource_capacity.resource_pool.pool_id
            resource_pool_response = await self.resource_pool_provider.get_resource(resource_pool_href)
            print("resource_pool_response!=", resource_pool_response)

            capacity_list = resource_pool_response.get("capacity")
            print("capacity_list", capacity_list)

            for capacity in capacity_list:
                print("capacity", capacity)
                resource_specification_list = capacity.get("resource_specification")
                capacity_amount_remaining, capacity_amount_from, capacity_amount_to, resource = \
                    await self.resource_pool_provider.extract_capacity_amount(capacity)
                related_party_id = await self.resource_pool_provider.extract_related_party(capacity)
                print("related_party_id", related_party_id)
                if related_party_id == "tinaa":
                    print("inside if")
                    demand_amount = int(reservation_item.reservation_resource_capacity.capacity_demand_amount)
                    reserved_vlans = \
                        await self._reserve_tinaa_resources(demand_amount,
                                                            int(capacity_amount_remaining),
                                                            used_vlans, resource)
                    print("reserved_vlans", reserved_vlans)
                    resource_inventory_response = \
                        await self.resource_inventory_provider.create_resource(related_party_id,
                                                                               reservation_item,
                                                                               resource_specification_list,
                                                                               reserved_vlans)
                    print("resource_inventory_response", resource_inventory_response)
                    resource_inventory_href = resource_inventory_response.get("href")
                    resource_inventory_id = resource_inventory_response.get("id")
                    # call PATCH Api for resource pool to update the capacity amount
                    tmf685_patch_response = await self.resource_pool_provider.patch_resource_pool(
                        resource_inventory_href,
                        resource_inventory_id,
                        resource_pool_id,
                        reserved_vlans, db)
                    log.info("tmf685_patch_response=%s", tmf685_patch_response)

                    reservation_res = \
                        await self.resource_pool_provider.create_resource_reservation_response(
                            reservation_create.reservation_item, used_vlans,
                            resource_inventory_href,
                            resource_inventory_id)
                    log.info("reservation_res=%s", reservation_res)
                    reservation_responses.append(reservation_res)

                elif related_party_id == "netcracker":
                    await self._reserve_netcracker_resources()
            return reservation_responses


resource_reservation_manager = ResourceReservationManager()
