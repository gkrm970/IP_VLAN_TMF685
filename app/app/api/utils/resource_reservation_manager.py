import uuid

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app import providers, schemas, log, models
from app.api import deps
from app.api.deps import get_db_session
from app.core.exceptions import InternalServerError
from app.providers.resource_pool_provider import final_reservation_response


class ResourceReservationManager:
    def __init__(self):
        self.resource_inventory_provider = providers.resource_inventory_provider
        self.resource_pool_provider = providers.resource_pool_provider

    async def _reserve_tinaa_resources(self, demand_amount: int, capacity_amount_remaining: int,
                                       capacity_amount_from: int, capacity_amount_to: int, used_vlans: set[int],
                                       resource):
        if demand_amount <= capacity_amount_remaining:
            available_capacity_amount = capacity_amount_remaining - demand_amount
            log.info(f"resource value: {resource}")
            if not resource:
                log.info(f"resource object is not empty: {resource}")
                unique_vlan_numbers = \
                    await self.resource_pool_provider.generate_unique_vlan(demand_amount, capacity_amount_from,
                                                                           capacity_amount_to, used_vlans)
                log.info(f"unique_vlan_numbers: {unique_vlan_numbers}")
                return unique_vlan_numbers, available_capacity_amount
        else:
            log.info("Not enough resources available to reserve VLANs.")
            raise InternalServerError("Not enough resources available to reserve VLANs.")

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(self, reservation_create: schemas.ReservationCreate, db: AsyncSession):
        used_vlans = set()
        reservation_responses = []
        for reservation_item in reservation_create.reservation_item:
            resource_pool_id = reservation_item.reservation_resource_capacity.resource_pool.pool_id

            result = await db.execute(
                select(models.ResourcePool).filter(
                    models.ResourcePool.id == resource_pool_id
                )
            )
            resource_pool_response = result.scalars().first().to_dict()
            log.info(f"resource_pool_response, {resource_pool_response}")

            # resource_pool_response = await self.resource_pool_provider.get_resource(resource_pool_href)
            capacity_list = resource_pool_response.get("capacity")
            log.info(f"capacity_list, {capacity_list}")
            for capacity in capacity_list:
                log.info("capacity", capacity)
                resource_specification_list = capacity.get("resource_specification")
                log.info(f"resource_specification_list: {resource_specification_list}")
                capacity_amount_remaining = capacity.get("capacity_amount_remaining")
                capacity_amount_from = capacity.get("capacity_amount_from")
                capacity_amount_to = capacity.get("capacity_amount_to")
                resource = capacity.get("resource")
                related_party_id = capacity.get("relatedParty").get("party_id")
                log.info("related_party_id_r", related_party_id)

                if related_party_id == "tinaa":
                    log.info("inside if")
                    demand_amount = int(reservation_item.reservation_resource_capacity.capacity_demand_amount)
                    reserved_vlans, available_capacity_amount = \
                        await self._reserve_tinaa_resources(demand_amount,
                                                            int(capacity_amount_remaining),
                                                            int(capacity_amount_from),
                                                            int(capacity_amount_to),
                                                            used_vlans, resource)
                    log.info("reserved_vlans", reserved_vlans)
                    resource_inventory_response = \
                        await self.resource_inventory_provider.create_resource(related_party_id,
                                                                               reservation_item,
                                                                               resource_specification_list,
                                                                               reserved_vlans)
                    print("resource_inventory_response_json", resource_inventory_response)

                    resource_inventory_href = resource_inventory_response.get("href")
                    resource_inventory_id = resource_inventory_response.get("id")

                    # Call PATCH Api for resource pool to update the capacity amount
                    resource_data = [
                        {"href": "http://ResourcePool/KJEKYR4YBKSB", "resource_id": "3473t4873tbskbcsbcks"}]
                    result = await db.execute(
                        select(models.ResourcePool).filter(
                            models.ResourcePool.id == resource_pool_id
                        )
                    )

                    resource_pool_response = result.scalars().first()
                    new_resource_data = models.ResourcePoolResource(
                        id=str(uuid.uuid4()),
                        resource_id="17r276r32763t26te",
                        href="http://ResourcePool/HF5R653R37R"
                    )

                    resource_pool_response.capacity[0].resource_pool_resource.append(new_resource_data)

                    await db.commit()
                    log.info("Update successfully resource_pool record data")

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
