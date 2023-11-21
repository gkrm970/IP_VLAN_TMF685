from app import providers, schemas, log


class ResourceReservationManager:
    def __init__(self):
        self.resource_pool_provider = providers.resource_pool_instance
        self.net_cracker_reservation_provider = (
            providers.net_cracker_reservation_instance
        )

    async def reserve(self, reservation_create: schemas.ReservationCreate):
        for reservation_item in reservation_create.reservation_item:
            resource_pool_href = (
                reservation_item.reservation_resource_capacity.resource_pool.href
            )
            resource_pool_id = (
                reservation_item.reservation_resource_capacity.resource_pool.pool_id
            )
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
            resource_pool_response = await self.resource_pool_provider.get_resource(
                resource_pool_href
            )
            capacity_list = resource_pool_response.get("capacity")

            if capacity_list:
                for capacity in capacity_list:
                    related_party_id = (
                        await self.resource_pool_provider.extract_related_party(
                            capacity
                        )
                    )
                    related_party_role = (
                        await self.resource_pool_provider.extract_related_party_role(
                            capacity
                        )
                    )
                    if related_party_id == "tinaa":
                        pass

                    elif related_party_id == "netcracker":
                        log.info(
                            "Entering into net cracker reserve IP address block if in case of "
                            "related party id is netcracker"
                        )
                        await self.net_cracker_reservation_provider.create_net_cracker_resource(
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


resource_reservation_manager = ResourceReservationManager()
