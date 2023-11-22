import uuid
from typing import Any, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import log, models, providers, settings


class NetCrackerPatchResourcePool:
    def __init__(self):
        self.api_base_url = settings.API_BASE_URL
        self.api_name = settings.API_NAME
        self.api_version = settings.API_VERSION
        self.ri_base_url = settings.RI_PROVIDER_BASE_URL
        self.ri_api_name = settings.RI_API_NAME
        self.ri_api_version = settings.RI_API_VERSION
        self.netcracker_release_ip_provider = providers.net_cracker_release_ip_instance

    async def _send_request(
        self, method, url: str, request_body: Optional[dict[str, Any]] = None
    ) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=request_body)
                response.raise_for_status()
                return response

        except httpx.HTTPError as e:
            log.error(f"HTTP Error: {e}")
            raise e
        except Exception as e:
            log.error(f"An error occurred: {e}")
            raise e

    async def netcracker_resource_pool_patch(
        self,
        reservation_item_resource_capacity_resource_pool_id,
        ip_names,
        resource_inventory_href,
        resource_inventory_id,
        resource_ip_id,
        db: AsyncSession,
    ):
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
                    id=str(uuid.uuid4()),
                    resource_id=resource_inventory_id,
                    href=resource_inventory_href,
                    characteristic=[[{"ipv4Subnet": ip_name} for ip_name in ip_names]],
                )

                resource_pool_response.capacity[0].resource_pool_resource.append(
                    new_resource_data
                )
                log.info("data_capacity_response=%s", resource_pool_response.to_dict())
                await db.commit()
            else:
                log.info(
                    f"ResourcePool with id {reservation_item_resource_capacity_resource_pool_id} not found."
                )

        except httpx.HTTPError as e:
            log.error(f"HTTP Error: {e}")
            # Roll back code for release IP address
            self.netcracker_release_ip_provider.release_ip(resource_ip_id, ip_names)
            log.info("Roll back of release IP address completed successfully")

            # Roll back code for resource inventory - delete
            if resource_inventory_id:
                url = (
                    f"{self.ri_base_url}{self.ri_api_name}/{self.ri_api_version}/resource/"
                    f"{resource_inventory_id}"
                )
                response = await self._send_request("DELETE", url)
                log.info("Resource inventory deleted successfully", response)
            raise e


net_cracker_resource_pool_patch_instance = NetCrackerPatchResourcePool()
