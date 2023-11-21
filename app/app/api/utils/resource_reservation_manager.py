import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app import providers, schemas, log, models
from app.core.exceptions import InternalServerError


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
                used_vlans.update(unique_vlan_numbers)
                return unique_vlan_numbers, available_capacity_amount
            else:
                remaining_demand = demand_amount - len(used_vlans)
                unique_vlan_numbers = \
                    await self.resource_pool_provider.generate_unique_vlan(remaining_demand, capacity_amount_from,
                                                                           capacity_amount_to, used_vlans)
                log.info(f"unique_vlan_numbers: {unique_vlan_numbers}")
                used_vlans.update(unique_vlan_numbers)
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

                    log.info("Update successfully resource_pool record data")
                    try:

                        result = await db.execute(
                            select(models.ResourcePool)
                            .options(selectinload(models.ResourcePool.capacity))
                            .filter(models.ResourcePool.id == resource_pool_id)
                        )

                        resource_pool_response = result.scalars().first()

                        if resource_pool_response:
                            resource_pool_response.capacity[0].capacity_amount_remaining = str(available_capacity_amount)
                            new_resource_data = models.ResourcePoolResource(
                                id=str(uuid.uuid4()),
                                resource_id="17r276r32763t26te",
                                href="http://ResourcePool/HF5R653R37R"
                            )

                            resource_pool_response.capacity[0].resource_pool_resource.append(new_resource_data)
                            print("data_capacity_response", resource_pool_response.to_dict())
                            await db.commit()
                        else:
                            print(f"ResourcePool with id {resource_pool_id} not found.")
                    except Exception as e:
                        delete_response = await self.resource_inventory_provider.delete_request(resource_inventory_id)
                        if delete_response.status_code == 204:
                            log.info(f'Deleted resource successfully with this id: {resource_inventory_id}')
                            raise InternalServerError(
                                f"update resource pool fails, an error occurred during resource pool updating {e}")
                        else:
                            print(f"Failed to delete resource. Status code: {delete_response.status_code}")

                    reservation_res = \
                        await self.resource_pool_provider.create_resource_reservation_response(
                            reservation_create, used_vlans,
                            resource_inventory_href,
                            resource_inventory_id)
                    log.info("reservation_res=%s", reservation_res)
                    reservation_responses.append(reservation_res)

                elif related_party_id == "netcracker":
                    await self._reserve_netcracker_resources()
            return reservation_responses


resource_reservation_manager = ResourceReservationManager()
