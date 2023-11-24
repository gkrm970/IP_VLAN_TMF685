import datetime
from typing import Any, Literal, TypeAlias

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from tenacity import retry, stop_after_attempt, wait_fixed

from app import log, models, providers, schemas, settings

Method: TypeAlias = Literal["GET", "POST", "PATCH", "DELETE"]


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def _send_request(
        method: Method,
        url: str,
        headers: dict[str, str] | None = None,
        request_body: dict[str, Any] | None = None,
) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, json=request_body)
        return response


class NCReserveIPProvider:
    def __init__(self):
        self.resource_name_id_from_nc = []
        self.resource_ip_id = str
        self.reserved_ips_names_from_nc = []
        self.resource_id_list = []
        self.nc_api_base_url = settings.NC_API_BASE_URL

    async def reserve_ip(
            self,
            reservation_item: schemas.ReservationItemCreate,
            related_party_id: str,
            related_party_role: str,
    ):
        create_resource_request_payload = {
            "relatedParty": {
                "partyRole": related_party_role,
                "partyId": related_party_id,
            },
            "@type": "IPRangeReservation",
            "requestedPeriod": {"fromToDateTime": str(datetime.datetime.now())},
            "reservationItem": [
                {
                    "quantity": reservation_item.quantity,
                    "@type": "IPRangeReservationItem",
                    "resourceCapacity": {
                        "@type": reservation_item.reservation_resource_capacity.type,
                        "capacityDemandAmount": (
                            reservation_item.reservation_resource_capacity.capacity_demand_amount
                        ),
                        "resourcePool": {
                            "@type": "IP Pool",
                            "id": reservation_item.reservation_resource_capacity.resource_pool.pool_id,
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
                                                for place_info in
                                                reservation_item.reservation_resource_capacity.reservation_place
                                            ],
                                            "characteristic": [
                                                {
                                                    "ipRangeCIDR": (
                                                        reservation_item.reservation_resource_capacity.capacity_demand_amount
                                                    ),
                                                    "addressPurpose": "Static",
                                                    "IPAMDescription": (
                                                        reservation_item.reservation_resource_capacity.external_party_characteristics.ipam_description
                                                    ),
                                                    "IPAMDetail": (
                                                        reservation_item.reservation_resource_capacity.external_party_characteristics.ipam_details
                                                    ),
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

        headers = {
            "Authorization": f"Bearer {await providers.nc_reserve_auth.get_access_token()}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }

        # Create net cracker reservation or Fetch the reserved IP address
        try:
            response = await _send_request(
                method="POST",
                url=nc_reservation_url,
                headers=headers,
                request_body=create_resource_request_payload
            )
            response.raise_for_status()
            json_data = response.json()
            if "reservationItem" in json_data:
                self.resource_ip_id = json_data["reservationItem"][0][
                    "appliedCapacityAmount"
                ]["resource"][0].get("id")

                for resource in json_data["reservationItem"][0][
                    "appliedCapacityAmount"
                ]["resource"]:
                    if resource.get("id") is not None:
                        self.resource_id_list.append(resource.get("id"))

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
                self.resource_name_id_from_nc.append(ip_names_ids)

                ip_names = [
                    resource.get("name")
                    for item in json_data.get("reservationItem", [])
                    for applied_capacity_amount in item.get("appliedCapacityAmount", {})
                    for resource in applied_capacity_amount.get("resource", [])
                    if resource.get("name") is not None
                ]
                self.reserved_ips_names_from_nc.append(ip_names)
                log.info(
                    "IP names from NC resource in list ",
                    self.reserved_ips_names_from_nc,
                )

                # Now, combined_data is a list of dictionaries with "id" and "name" pairs
                log.info("combined_data from NC resource ", ip_names_ids)
                return self.resource_id_list, ip_names_ids

        except httpx.RequestError as exc:
            log.error(
                "Failed to create net cracker reservation or failed to reserve IP:"
                f" {exc}"
            )
            raise Exception(f"Failed to create net cracker reservation: {exc}")


nc_reserve_ip_instance = NCReserveIPProvider()


class NCReleaseIPProvider:
    def __init__(self):
        self.nc_api_base_url = settings.NC_API_BASE_URL

    async def release_ip(
            self,
    ) -> httpx.Response:
        # Access reserved_ips from the nc_reserve_ip_instance
        payload = {
            "@baseType": "Network",
            "@type": "IP Range",
            "id": nc_reserve_ip_instance.resource_ip_id,
            "name": [
                ip_name for ip_name in nc_reserve_ip_instance.reserved_ips_names_from_nc
            ],
            "resourceCharacteristic": [
                {
                    "id": resource_id_from_nc,
                    "name": "Status",
                    "value": "UNASSIGNED",
                    "valueType": "Text",
                }
                for resource_id_from_nc in nc_reserve_ip_instance.resource_id_list
            ],
        }

        # Release IP address request
        nc_release_ip_url = (
            f"{self.nc_api_base_url}/resource/ncResourceInventoryManagement/v1/resource/"
            f"{nc_reserve_ip_instance.resource_ip_id}"
        )
        headers = {
            "Authorization": f"Bearer {await providers.nc_release_auth.get_access_token()}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        try:
            response = await _send_request(
                method="PATCH",
                url=nc_release_ip_url,
                headers=headers,
                request_body=payload)
            return response
        except httpx.RequestError as exc:
            log.error(f"Failed to release IP address: {exc}")
            raise Exception(f"Failed to release IP address: {exc}")


nc_release_ip_instance = NCReleaseIPProvider()


class ResourceInventoryProvider:
    def __init__(self):
        self.ri_api_base_url = str(settings.RI_BASE_URL)
        self.ri_api_name = settings.RI_API_NAME
        self.ri_api_version = settings.RI_API_VERSION

    async def create_resource_inventory(
            self,
            reservation_create: schemas.ReservationItemCreate,
            resource_specification_list: list,
    ) -> None | dict | Any:
        reservation_place = (
            reservation_create.reservation_item.reservation_resource_capacity.reservation_place
        )

        create_resource_request = {
            "category": "ipv4Subnet_Resource",
            "description": "ipv4Subnet",
            "name": "pcg-loopback-pc-up-N6_SGi_IMS_v4",
            "operationalState": "enable",
            "resourceCharacteristic": [],
            "resourceSpecification": [],
            "resourceVersion": "0.0.1",
            "place": [],
        }
        # Reserved IP name and ID from net cracker are appended to the resourceCharacteristic list
        for name_id in nc_reserve_ip_instance.resource_name_id_from_nc:
            create_resource_request["resourceCharacteristic"].append(
                {
                    "id": name_id.get("id"),
                    "name": name_id.get("name"),
                }
            )

        for place_info in reservation_place:
            create_resource_request["place"].append(
                {"name": place_info.name, "role": place_info.type}
            )
        # Resource specification info from resource pool is appended to the resourceSpecification list
        for resource_specification_info in resource_specification_list:
            create_resource_request["resourceSpecification"].append(
                {
                    "href": resource_specification_info.get("href"),
                    "id": resource_specification_info.get("id"),
                    "version": "0.0.1",
                }
            )

        # Create resource inventory request
        tmf_639_url = (
            f"{self.ri_api_base_url}/{self.ri_api_name}/{self.ri_api_version}/resource"
        )
        try:
            resource_inventory_response = await _send_request(
                method="POST",
                url=tmf_639_url,
                request_body=create_resource_request
            )
            log.info(
                "Resource inventory created successfully", resource_inventory_response
            )
            resource_inventory_response.raise_for_status()
            log.info("Resource inventory created successfully %s")
            resource_inventory_response.json().get("href")
            resource_inventory_response.json().get("id")
            return resource_inventory_response
        except httpx.HTTPStatusError as e:
            log.error("HTTPStatusError", e)
            log.exception("Could not able to create resource and raised exception", e)
            # Roll back the net cracker release ip
            await nc_release_ip_instance.release_ip()
            raise e


nc_resource_inventory_instance = ResourceInventoryProvider()


class ResourcePoolPatchProvider:
    def __init__(self):
        self.api_base_url = settings.API_BASE_URL
        self.api_name = settings.API_NAME
        self.api_version = settings.API_VERSION
        self.ri_base_url = str(settings.RI_BASE_URL)
        self.ri_api_name = settings.RI_API_NAME
        self.ri_api_version = settings.RI_API_VERSION

    async def resource_pool_patch(
            self,
            reservation_item_resource_capacity_resource_pool_id: str,
            ip_names: list[str],
            resource_inventory_href: str,
            resource_inventory_id: str,
            db: AsyncSession,
    ) -> None | dict | Any:
        try:
            result = await db.execute(
                select(models.ResourcePool)
                .options(selectinload(models.ResourcePool.capacity))
                .filter(
                    models.ResourcePool.id
                    == reservation_item_resource_capacity_resource_pool_id
                )
            )

            resource_pool_response = result.scalars().first()

            if resource_pool_response:
                new_resource_data = models.ResourcePoolResource(
                    resource_id=resource_inventory_id,
                    href=resource_inventory_href,
                    characteristic=[[{"ipv4Subnet": ip_name} for ip_name in ip_names]],
                )

                resource_pool_response.capacity[0].resource_pool_resource.append(
                    new_resource_data
                )
                log.info("data_capacity_response=%s", resource_pool_response.to_dict())
                await db.commit()
                return resource_pool_response.to_dict()
            else:
                log.info(
                    "ResourcePool with id"
                    f" {reservation_item_resource_capacity_resource_pool_id} not found."
                )

        except httpx.HTTPError as e:
            log.error(f"Unable to patch resource pool, HTTP Error: {e}")
            # Roll-back code for release IP address
            await nc_release_ip_instance.release_ip()
            log.info("Roll back of release IP address completed successfully")

            # Roll back code for resource inventory - delete
            if resource_inventory_id:
                url = (
                    f"{self.ri_base_url}{self.ri_api_name}/{self.ri_api_version}/resource/"
                    f"{resource_inventory_id}"
                )
                response = await _send_request(
                    method="DELETE",
                    url=url
                )
                log.info("Resource inventory deleted successfully", response)
                response.raise_for_status()
            raise e
        return resource_pool_response


resource_pool_patch_instance = ResourcePoolPatchProvider()
