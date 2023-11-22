from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from app import log, providers, settings


# Decorate the asynchronous function with retry logic
@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def make_patch_request(url, payload):
    auth_header = await providers.nc_auth.get_header()

    headers = {
        **auth_header,
        "Content-Type": "application/json",
        "accept": "application/json",
        "env": "it02",
    }

    async with httpx.AsyncClient() as session:
        response = await session.patch(url, headers=headers, json=payload)
        response.raise_for_status()  # Check if the request was successful
        return response


class NetCrackerReleaseIPProvider:
    def __init__(self):
        self.nc_api_base_url = settings.NC_API_BASE_URL

    async def release_ip(
        self,
        resource_ip_id,
        ip_names,
    ) -> None | dict | Any:
        payload = {
            "@baseType": "Network",
            "@type": "IP Range",
            "id": resource_ip_id,
            "name": [ip_name for ip_name in ip_names],
            "resourceCharacteristic": [
                {
                    "id": resource_ip_id,
                    "name": "Status",
                    "value": "UNASSIGNED",
                    "valueType": "Text",
                }
            ],
        }

        # Release IP address request
        netcracker_release_ip_url = (
            f"{self.nc_api_base_url}/resource/ncResourceInventoryManagement/v1/resource/"
            f"{resource_ip_id}"
        )
        try:
            response = await make_patch_request(netcracker_release_ip_url, payload)
            return response
        except httpx.RequestError as exc:
            log.error(f"Failed to release IP address: {exc}")
            return exc


net_cracker_release_ip_instance = NetCrackerReleaseIPProvider()
