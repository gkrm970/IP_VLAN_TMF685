from app import providers, schemas, log
from app.core.exceptions import InternalServerError
from app.providers.resource_pool_provider import final_reservation_response


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
                unique_vlan = await self.resource_pool_provider.generate_unique_vlan(capacity_amount, used_vlans)
                if unique_vlan is not None:
                    reserved_vlans.add(unique_vlan)
            return reserved_vlans
        else:
            print("Not enough resources available to reserve VLANs.")
            raise InternalServerError("Not enough resources available to reserve VLANs.")

    async def _reserve_netcracker_resources(self):
        pass

    async def reserve(self, reservation_create: schemas.ReservationCreate):
        used_vlans = set()
        reservation_responses = []
        for reservation_item in reservation_create.reservation_item:
            resource_pool_href = reservation_item.reservation_resource_capacity.resource_pool.href
            resource_pool_id = reservation_item.reservation_resource_capacity.resource_pool.pool_id
            resource_pool_response = await self.resource_pool_provider.get_resource(resource_pool_href)
            capacity_list = resource_pool_response.get("capacity")

            for capacity in capacity_list:
                resource_specification_list = capacity.get("resourceSpecification")
                capacity_amount = await self.resource_pool_provider.extract_capacity_amount(capacity)
                related_party_id = await self.resource_pool_provider.extract_related_party(capacity)
                if related_party_id == "tinaa":
                    demand_amount = int(reservation_item.reservation_resource_capacity.capacity_demand_amount)
                    reserved_vlans = await self._reserve_tinaa_resources(demand_amount, int(capacity_amount),
                                                                         used_vlans)
                    resource_inventory_response = \
                        await self.resource_inventory_provider.create_resource(related_party_id, reserved_vlans,
                                                                               reservation_item,
                                                                               resource_specification_list)
                    resource_inventory_href = resource_inventory_response.get("href")
                    resource_inventory_id = resource_inventory_response.get("id")
                    reservation_res = \
                        await self.resource_pool_provider.create_resource_reservation_response(
                            reservation_create.reservation_item, used_vlans,
                            resource_inventory_href,
                            resource_inventory_id)
                    reservation_responses.append(reservation_res)

                elif related_party_id == "netcracker":
                    await self._reserve_netcracker_resources()
            return reservation_responses


resource_reservation_manager = ResourceReservationManager()
