import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import crud, log, models, providers, schemas
from app.core.exceptions import BadRequestError, InternalServerError


class ResourceReservationManager:
    def __init__(self):
        self.resource_specification_list = []
        self.resource_inventory_provider = providers.resource_inventory_provider
        self.resource_pool_provider = providers.resource_pool_provider
        self.net_cracker_reservation_provider = providers.nc_reserve_ip_instance

    async def _reserve_tinaa_resources(
        self,
        demand_amount: int,
        capacity_amount_remaining: int,
        capacity_amount_from: int,
        capacity_amount_to: int,
        used_vlans: list,
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
                return unique_vlan_numbers, available_capacity_amount
            else:
                unique_vlan_numbers = (
                    await self.resource_pool_provider.generate_unique_vlan(
                        demand_amount,
                        capacity_amount_from,
                        capacity_amount_to,
                        used_vlans,
                    )
                )
                log.info("unique_vlan_numbers=%s", unique_vlan_numbers)
            return unique_vlan_numbers, available_capacity_amount
        else:
            log.info("Not enough resources available to reserve VLANs.")
            raise BadRequestError("Not enough resources available to reserve VLANs.")

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(
        self, reservation_create: schemas.ReservationCreate, db: AsyncSession
    ):
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
            resource_pool: models.ResourcePool | None = result.scalars().first()

            if resource_pool is None:
                raise BadRequestError("Resource pool not found")

            resource_pool_data = resource_pool.to_dict()
            log.info("resource_pool_response=%s", resource_pool)
            capacity_list = resource_pool_data.get("capacity")
            log.info("capacity_list=%s", capacity_list)

            for capacity in capacity_list:
                log.info("capacity", capacity)
                resource_specification_list = capacity.get("resourceSpecification")
                log.info(f"resource_specification_list: {resource_specification_list}")
                capacity_amount_remaining = capacity.get("capacityAmountRemaining")
                capacity_amount_from = capacity.get("capacityAmountFrom")
                capacity_amount_to = capacity.get("capacityAmountTo")
                resource = capacity.get("resource")
                related_party_id = capacity.get("relatedParty").get("party_id")
                log.info("related_party_id=%s", related_party_id)
                related_party_role = capacity.get("relatedParty").get("party_role")
                log.info("related_party_id=%s", related_party_id)

                if related_party_id == "tinaa":
                    log.info("inside if")
                    demand_amount = int(
                        reservation_item.reservation_resource_capacity.capacity_demand_amount
                    )
                    vlans = await db.execute(
                        select(models.VlanAllocation.used_vlan_numbers)
                    )
                    results = vlans.fetchall()
                    if results is not None:
                        used_vlans = [
                            vlan_number
                            for vlan_set, in results
                            for vlan_number in vlan_set
                        ]
                    else:
                        used_vlans = []
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
                    vlan_object = models.VlanAllocation(
                        id=str(uuid.uuid4()), used_vlan_numbers=reserved_vlans,
                        resource_pool_id=resource_pool_id
                    )
                    vlan_id = vlan_object.id
                    db.add(vlan_object)
                    await db.commit()
                    log.info("vlan_object=%s", used_vlans)
                    log.info("reserved_vlans_1=%s", reserved_vlans)
                    resource_inventory_response = (
                        await self.resource_inventory_provider.create_resource(
                            reservation_item,
                            resource_specification_list,
                            reserved_vlans,
                            vlan_id,
                            db,
                        )
                    )
                    log.info(
                        resource_inventory_response,
                    )

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
                            resource_pool_response.capacity[
                                0
                            ].capacity_amount_remaining = str(available_capacity_amount)
                            new_resource_data = models.ResourcePoolResource(
                                id=str(uuid.uuid4()),
                                resource_id=resource_inventory_id,
                                href=resource_inventory_href,
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
                        await db.execute(
                            delete(models.VlanAllocation).where(
                                models.VlanAllocation.id == vlan_id
                            )
                        )
                        await db.commit()
                        delete_response = await self.resource_inventory_provider.delete_resource_by_id(
                            resource_inventory_id
                        )
                        if delete_response.status_code == 204:
                            log.info(
                                "Deleted resource successfully with this id=%s",
                                resource_inventory_id,
                            )
                            raise InternalServerError(
                                f"update resource pool fails, an error "
                                f"occurred during resource pool updating {e}"
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
                    )

                log.info("Before reservation creation")
                reservation = await crud.reservation.create(
                    db,
                    reservation_create,
                    href=resource_inventory_href,
                    _id=resource_inventory_id,
                    vlans=reserved_vlans,
                )
                log.info("After reservation creation")
        return reservation


resource_reservation_manager = ResourceReservationManager()
