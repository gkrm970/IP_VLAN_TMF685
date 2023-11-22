import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import crud, log, models, providers, schemas
from app.core.exceptions import InternalServerError


class ResourceReservationManager:
    def __init__(self):
        self.resource_inventory_provider = providers.resource_inventory_provider
        self.resource_pool_provider = providers.resource_pool_provider
        self.net_cracker_reservation_provider = (
            providers.net_cracker_reservation_instance
        )

    async def _reserve_tinaa_resources(
        self,
        demand_amount: int,
        capacity_amount_remaining: int,
        capacity_amount_from: int,
        capacity_amount_to: int,
        used_vlans: set[int],
        resource,
    ):
        if demand_amount <= capacity_amount_remaining:
            available_capacity_amount = capacity_amount_remaining - demand_amount
            log.info("resource value=%s", resource)
            if not resource:
                log.info("resource object is not empty=%s", resource)
                unique_vlan_numbers = (
                    await self.resource_pool_provider.generate_unique_vlan(
                        demand_amount,
                        capacity_amount_from,
                        capacity_amount_to,
                        used_vlans,
                    )
                )
                log.info("unique_vlan_numbers=%s", unique_vlan_numbers)
                used_vlans.update(unique_vlan_numbers)
                return unique_vlan_numbers, available_capacity_amount
            else:
                remaining_demand = demand_amount - len(used_vlans)
                unique_vlan_numbers = (
                    await self.resource_pool_provider.generate_unique_vlan(
                        remaining_demand,
                        capacity_amount_from,
                        capacity_amount_to,
                        used_vlans,
                    )
                )
                log.info("unique_vlan_numbers=%s", unique_vlan_numbers)
                used_vlans.update(unique_vlan_numbers)
                return unique_vlan_numbers, available_capacity_amount
        else:
            log.info("Not enough resources available to reserve VLANs.")
            raise InternalServerError(
                "Not enough resources available to reserve VLANs."
            )

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(
        self, reservation_create: schemas.ReservationCreate, db: AsyncSession
    ):
        used_vlans = set()
        reservation = []
        for reservation_item in reservation_create.reservation_item:
            resource_pool_id = (
                reservation_item.reservation_resource_capacity.resource_pool.pool_id
            )

            result = await db.execute(
                select(models.ResourcePool).filter(
                    models.ResourcePool.id == resource_pool_id
                )
            )
            resource_pool_response = result.scalars().first().to_dict()
            log.info("resource_pool_response=%s", resource_pool_response)
            capacity_list = resource_pool_response.get("capacity")
            log.info("capacity_list=%s", capacity_list)

            # Variables for net cracker payload
            reservation_item_quantity = reservation_item.quantity
            reservation_item_resource_capacity_type = (
                reservation_item.reservation_resource_capacity.type
            )
            reservation_item_resource_capacity_capacity_demand_amount = (
                reservation_item.reservation_resource_capacity.capacity_demand_amount
            )
            reservation_item_resource_capacity_resource_pool_id = (
                reservation_item.reservation_resource_capacity.resource_pool.pool_id
            )
            ipam_description = (
                reservation_item.reservation_resource_capacity.external_party_characteristics.ipam_description
            )
            ipam_detail = (
                reservation_item.reservation_resource_capacity.external_party_characteristics.ipam_details
            )
            # end here

            for capacity in capacity_list:
                log.info("capacity=%s", capacity)
                resource_specification_list = capacity.get("resource_specification")
                log.info("resource_specification_list=%s", resource_specification_list)
                capacity_amount_remaining = capacity.get("capacity_amount_remaining")
                capacity_amount_from = capacity.get("capacity_amount_from")
                capacity_amount_to = capacity.get("capacity_amount_to")
                resource = capacity.get("resource")
                related_party_id = capacity.get("relatedParty").get("party_id")
                log.info("related_party_id=%s", related_party_id)
                related_party_role = capacity.get("relatedParty").get("party_role")

                if related_party_id == "tinaa":
                    log.info("inside if")
                    demand_amount = int(
                        reservation_item.reservation_resource_capacity.capacity_demand_amount
                    )
                    (
                        reserved_vlans,
                        available_capacity_amount,
                    ) = await self._reserve_tinaa_resources(
                        demand_amount,
                        int(capacity_amount_remaining),
                        int(capacity_amount_from),
                        int(capacity_amount_to),
                        used_vlans,
                        resource,
                    )
                    log.info("reserved_vlans=%s", reserved_vlans)
                    resource_inventory_response = (
                        await self.resource_inventory_provider.create_resource(
                            reservation_item,
                            resource_specification_list,
                            reserved_vlans,
                        )
                    )
                    log.info(
                        "resource_inventory_response_json=%s",
                        resource_inventory_response,
                    )

                    resource_inventory_response.get("href")
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
                            resource_pool_response.capacity[
                                0
                            ].capacity_amount_remaining = str(available_capacity_amount)
                            new_resource_data = models.ResourcePoolResource(
                                id=str(uuid.uuid4()),
                                resource_id="17r276r32763t26te",
                                href="http://ResourcePool/HF5R653R37R",
                            )

                            resource_pool_response.capacity[
                                0
                            ].resource_pool_resource.append(new_resource_data)
                            log.info(
                                "data_capacity_response=%s",
                                resource_pool_response.to_dict(),
                            )
                            await db.commit()
                        else:
                            log.info(
                                f"ResourcePool with id {resource_pool_id} not found."
                            )
                    except Exception as e:
                        log.info(f"{e}")
                        delete_response = (
                            await self.resource_inventory_provider.delete_request(
                                resource_inventory_id
                            )
                        )
                        if delete_response.status_code == 204:
                            log.info(
                                "Deleted resource successfully with this id=%s",
                                resource_inventory_id,
                            )
                            raise InternalServerError(
                                f"update resource pool fails, an error occurred during resource pool updating {e}"
                            )
                        else:
                            log.info(
                                "Failed to delete resource Status code=%s",
                                delete_response.status_code,
                            )
                elif related_party_id == "netcracker":
                    log.info(
                        "Entering into net cracker reserve IP address block if in case of "
                        "related party id is netcracker"
                    )
                    await self.net_cracker_reservation_provider.reserve_ip(
                        reservation_item,
                        related_party_id,
                        related_party_role,
                        reservation_item_quantity,
                        reservation_item_resource_capacity_capacity_demand_amount,
                        reservation_item_resource_capacity_type,
                        reservation_item_resource_capacity_resource_pool_id,
                        ipam_description,
                        ipam_detail,
                    )

                log.info("Before reservation creation")
                reservation = await crud.reservation.create(db, reservation_create)
                log.info("After reservation creation")
        return reservation


resource_reservation_manager = ResourceReservationManager()
