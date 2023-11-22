import datetime
from typing import Any, List, Tuple

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from app import log, providers, settings


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def make_post_request(url: str, payload: dict) -> httpx.Response:
    auth_header = await providers.nc_auth.get_header()

    headers = {
        **auth_header,
        "Content-Type": "application/json",
        "accept": "application/json",
        "env": "it02",
    }

    async with httpx.AsyncClient() as session:
        response = await session.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Check if the request was successful
        return response


class NetCrackerReservationProvider:
    def __init__(self):
        self.nc_api_base_url = settings.NC_API_BASE_URL
        self.netcracker_resource_inventory_provider = (
            providers.net_cracker_resource_inventory_instance
        )
        self.netcarcker_release_ip_provider = providers.net_cracker_release_ip_instance
        self.netcracker_resource_pool_patch_provider = (
            providers.net_cracker_resource_pool_patch_instance
        )
        self.reserves_ips: List[Any] = []

    async def reserve_ip(
        self,
        reservation_item: Any,
        related_party_id: str,
        related_party_role: str,
        reservation_item_quantity: str,
        reservation_item_resource_capacity_type: str,
        reservation_item_resource_capacity_capacity_demand_amount: str,
        reservation_item_resource_capacity_resource_pool_id: str,
        ipam_description: str,
        ipam_detail: str,
        resource_specification_list: List[Any],
    ) -> Tuple[List[dict[str, Any]], Any, List[Any]]:
        resource_ip_id = None
        ip_names_ids = None
        reservation_place = (
            reservation_item.reservation_resource_capacity.reservation_place
        )

        create_resource_request_payload = {
            "relatedParty": {
                "partyRole": related_party_role,
                "partyId": related_party_id,
            },
            "@type": "IPRangeReservation",
            "requestedPeriod": {"fromToDateTime": str(datetime.datetime.now())},
            "reservationItem": [
                {
                    "quantity": reservation_item_quantity,
                    "@type": "IPRangeReservationItem",
                    "resourceCapacity": {
                        "@type": reservation_item_resource_capacity_type,
                        "capacityDemandAmount": reservation_item_resource_capacity_capacity_demand_amount,
                        "resourcePool": {
                            "@type": "IP Pool",
                            "id": reservation_item_resource_capacity_resource_pool_id,
                            "resourceCollection": [
                                {
                                    "@type": "IP Pool",
                                    "name": "True Static IP",
                                    "resource": [
                                        {
                                            "preferredSubnet": "",
                                            "place": [
                                                {
                                                    "name": place_info.name,
                                                    "role": place_info.type,
                                                }
                                                for place_info in reservation_place
                                            ],
                                            "characteristic": [
                                                {
                                                    "ipRangeCIDR": reservation_item_resource_capacity_capacity_demand_amount,
                                                    # capacity demand amount
                                                    "addressPurpose": "Static",
                                                    "IPAMDescription": ipam_description,
                                                    "IPAMDetail": ipam_detail,
                                                    "Customer": {
                                                        "name": "TEST CUSTOMER 11",
                                                        "cpid": "77000001",
                                                        "streetAddress": "2C 4816 50 AVE",
                                                        "province": "AB",
                                                        "postalCode": None,
                                                        "country": None,
                                                        "city": None,
                                                        "lpdsid": None,
                                                    },
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                }
            ],
        }
        nc_reservation_url = (
            f"{self.nc_api_base_url}/resource/resourcePoolManagement/v1/reservation"
        )

        try:
            response = await make_post_request(
                nc_reservation_url, create_resource_request_payload
            )
            response.raise_for_status()
            json_data = response.json()
            if "reservationItem" in json_data:
                resource_ip_id = json_data["reservationItem"][0][
                    "appliedCapacityAmount"
                ]["resource"][0].get("id")

                data = json_data.get("reservationItem", [])

                # Extract the id and name from the resource list
                ip_names_ids = [
                    {"id": resource.get("id"), "name": resource.get("name")}
                    for item in data
                    for applied_capacity_amount in item.get("appliedCapacityAmount", {})
                    for resource in applied_capacity_amount.get("resource", [])
                    if resource.get("id") is not None
                    and resource.get("name") is not None
                ]
                ip_names = [
                    resource.get("name")
                    for item in json_data.get("reservationItem", [])
                    for applied_capacity_amount in item.get("appliedCapacityAmount", {})
                    for resource in applied_capacity_amount.get("resource", [])
                    if resource.get("name") is not None
                ]
                log.info("ip_names from NC resource ", ip_names)

                # Now, combined_data is a list of dictionaries with "id" and "name" pairs
                log.info("combined_data from NC resource ", ip_names_ids)
                return ip_names_ids, resource_ip_id, ip_names

        except httpx.RequestError as exc:
            log.error(f"Failed to create net cracker reservation: {exc}")
            raise Exception(f"Failed to create net cracker reservation: {exc}")

        # Create resource inventory and update resource pool
        try:
            # Create resource inventory
            resource_inventory_response = (
                await self.netcracker_resource_inventory_provider.create_resource(
                    ip_names_ids,
                    resource_ip_id,
                    reservation_item,
                    resource_specification_list,
                )
            )
            resource_inventory_response.raise_for_status()
            log.info("Resource inventory created successfully %s")
            resource_inventory_href = resource_inventory_response.json().get("href")
            resource_inventory_id = resource_inventory_response.json().get("id")

            # Partial update resourcePool
            resource_pool_response = await self.netcracker_resource_pool_patch_provider.patch_resource_pool_netcracker(
                reservation_item_resource_capacity_resource_pool_id,
                ip_names_ids,
                resource_inventory_href,
                resource_inventory_id,
                resource_ip_id,
            )
            resource_pool_response.raise_for_status()
            log.info("Resource pool updated successfully %s", resource_pool_response)

        except httpx.RequestError as exc:
            log.error(f"Error creating resource inventory {exc}")
            # Perform rollback here for net cracker reservation
            self.netcarcker_release_ip_provider.release_ip(resource_ip_id, ip_names_ids)
            log.info("Rollback of release IP address completed successfully")
            raise Exception(
                f"Error creating resource inventory or updating resource pool: {exc}"
            )


net_cracker_reservation_instance = NetCrackerReservationProvider()
