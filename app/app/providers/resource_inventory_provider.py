from typing import Any

import httpx

from app.core.config import settings
class ResourceInventoryProvider:
    def __init__(self):
        self.base_url = settings.RI_PROVIDER_BASE_URL
        self.api_prefix = settings.RI_PROVIDER_API_PREFIX

    async def _send_request(self, method, url:str, request_body: dict[str, Any] | None) -> httpx.Response:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=request_body)

                response.raise_for_status()

        except httpx.HTTPStatusError:
            pass
        except httpx.RequestError:
            pass

    async def create_resource(self, request_body: dict[str, Any]) -> dict[str, Any]:
        response = await self._send_request("POST", urljoin(self.base_url, "resource"), request_body)

        return response.json()

    async def get_resource(self, id: str) -> dict[str, Any]:
        response = await self._send_request("GET", ulrjoin(self.base_url, f"resource/{id}"))
        return response.json()

resource_inventory_provider = ResourceInventoryProvider()
