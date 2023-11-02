from app import providers, schemas, log


class ResourceReservationManager:
    def __init__(self):
        self.resource_inventory_provider = providers.resource_inventory_provider
        self.resource_pool_provider = providers.resource_pool_provider

    async def _reserve_tinaa_resources(self, demand_amount: int, capacity_amount: int, used_vlans: set[int]):
        reserved_vlans = set()
        if demand_amount <= capacity_amount:
            available_capacity_amount = capacity_amount - demand_amount
            # schemas.ResourcePoolManagementUpdate.resource_capacity.capacity_amount = available_capacity_amount
            for _ in range(demand_amount):
                unique_vlan = self.resource_pool_provider.generate_unique_vlan(capacity_amount, used_vlans)
                if unique_vlan is not None:
                    reserved_vlans.add(unique_vlan)
            return reserved_vlans

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(self, reservation_create: schemas.ReservationCreate):
        used_vlans = set()
        resource_inventory_href = None  # Initialize with a default value
        resource_inventory_id = None  # Initialize with a default value

        for reservation_item in reservation_create.reservation_item:
            resource_pool_href = reservation_item.reservation_resource_capacity.resource_pool.href
            resource_pool_id = reservation_item.reservation_resource_capacity.resource_pool.pool_id
            resource_pool_response = await self.resource_pool_provider.get_resource(resource_pool_href)
            log.info(f"resource_pool_response: {resource_pool_response}")
            capacity_list = resource_pool_response.get("capacity")
            log.info("capacity_list", capacity_list)
            for capacity in capacity_list:
                capacity_amount = await self.resource_pool_provider.extract_capacity_amount(capacity)
                log.info("capacity_amount", capacity_amount)
                related_party_id = await self.resource_pool_provider.extract_related_party(capacity)

                if related_party_id == "TINAA":
                    log.info("Inside If")
                    demand_amount = int(reservation_item.reservation_resource_capacity.capacity_demand_amount)
                    reserved_vlans = await self._reserve_tinaa_resources(demand_amount, capacity_amount, used_vlans)
                    are_enough_vlans_available = len(reserved_vlans) == demand_amount
                    if are_enough_vlans_available:
                        resource_inventory_response = \
                            await self.resource_inventory_provider.create_resource(related_party_id, reserved_vlans)
                        resource_inventory_href = resource_inventory_response.get("href")
                        resource_inventory_id = resource_inventory_response.get("id")
                elif related_party_id == "netcracker":
                    await self._reserve_netcracker_resources()
                reservation_response = \
                    self.resource_pool_provider.create_resource_reservation_response(reservation_create.reservation_item, used_vlans,
                                                                                     resource_inventory_href,
                                                                                     resource_inventory_id)
                log.info(f"reservation_response: {reservation_response}")
                return await reservation_response


resource_reservation_manager = ResourceReservationManager()
