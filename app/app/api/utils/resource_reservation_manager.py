from app import providers, schemas


class ResourceReservationManager:
    def __init__(self):
        self.resource_inventory_provider = providers.resource_inventory_provider



    def _reserve_tinaa_resources(self):
        pass

    def _reserve_netcracker_resources(self):
        pass

    async def reserve(self, reservation_create: schemas.ReservationCreate) -> None:
        self.resource_inventory_provider.create_resource()


resource_reservation_manager = ResourceReservationManager()
