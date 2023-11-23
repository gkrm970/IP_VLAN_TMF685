import threading
import time
from typing import TypedDict

from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import HTTPException, status

from app import log
from app.core.config import settings


class AuthHeader(TypedDict):
    Authorization: str


class NetCrackerAuthProvider:
    def __init__(self):
        self._token_update_time: int | None = None

        self.oauth_client = AsyncOAuth2Client(
            client_id=settings.NC_CLIENT_ID,
            client_secret=settings.NC_CLIENT_SECRET,
        )

        self.lock = threading.Lock()

    @property
    def access_token(self) -> str:
        return self.oauth_client.token["access_token"]

    @property
    def expires_in(self) -> int:
        return self.oauth_client.token["expires_in"]

    @property
    def token_update_time(self) -> int | None:
        return self._token_update_time

    @token_update_time.setter
    def token_update_time(self, value: int) -> None:
        self._token_update_time = value

    def _is_token_about_to_expire(self) -> bool:
        if self.access_token is None or self.token_update_time is None:
            log.debug("The access_token or token_update_time is None")
            return True

        else:
            time_elapsed = int(time.time()) - self.token_update_time
            log.debug(
                f"Token expiration info: token_update_time: {self.token_update_time}, "
                f"expires_in: {self.expires_in}, time_elapsed: {time_elapsed}"
            )

        return self.expires_in < (time_elapsed + 60)

    async def _fetch_access_token(self) -> None:
        log.debug("Fetching access token")
        try:
            await self.oauth_client.fetch_token(
                url=str(settings.NC_TOKEN_URL),
                grant_type="client_credentials",
            )
            self.token_update_time = int(time.time())
            log.debug("Access token fetched successfully")

        except Exception as exc:
            log.error(f"Failed to fetch access token: {exc}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="External API communication error",
            )

    async def get_access_token(self, force_new: bool = False) -> str:
        with self.lock:
            if force_new or self.token_update_time is None:
                log.debug(f"Fetching new access token, {force_new=}")

                await self._fetch_access_token()

                return self.access_token

            if self._is_token_about_to_expire():
                log.debug("Fetching new access token, token is about to expire")

                await self._fetch_access_token()

            return self.access_token

    async def get_header(self, force_new: bool = False) -> AuthHeader:
        return {"Authorization": f"Bearer {await self.get_access_token(force_new)}"}


nc_auth = NetCrackerAuthProvider()
