from typing import Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from app import log, providers
from app.core.config import settings


class NetCrackerResourceInventoryProvider:
    def __init__(self):
        self.ri_api_base_url = settings.RI_API_BASE_URL
        self.ri_api_name = settings.RI_API_NAME
        self.ri_api_version = settings.RI_API_VERSION
        self.netcracker_release_ip_provider = providers.net_cracker_release_ip_instance

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def _send_request(
        self, method, url: str, request_body: Optional[dict[str, Any]] = None
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=request_body)
            response_639 = response.json()

        return response_639

    async def create_resource(
        self,
        reservation_item,
        resource_specification_list,
        resource_ip_id,
        ip_names_ids,
    ) -> None | dict | Any:
        reservation_place = (
            reservation_item.reservation_resource_capacity.reservation_place
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

        for name_id in ip_names_ids:
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

        for resource_specification_info in resource_specification_list:
            create_resource_request["resourceSpecification"].append(
                {
                    "href": resource_specification_info.get("href"),
                    "id": resource_specification_info.get("id"),
                    "version": "0.0.1",
                }
            )

        # Create resource inventory request
        tmf_639_url = f"{self.ri_api_base_url}/{self.ri_api_name}/{self.ri_api_version}/resource"
        try:
            response = await self._send_request(
                "POST", tmf_639_url, create_resource_request
            )
            log.info("Resource inventory created successfully", response)
            return response
        except httpx.HTTPStatusError as e:
            log.error("HTTPStatusError", e)
            log.exception("Could not able to create resource and raised exception", e)
            # Roll back the net cracker release ip
            await self.netcracker_release_ip_provider.release_ip(
                resource_ip_id, ip_names_ids
            )

            raise e


net_cracker_resource_inventory_instance = NetCrackerResourceInventoryProvider()
