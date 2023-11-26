import threading
import time
from typing import TypedDict

import aiohttp
from authlib.integrations.httpx_client import AsyncOAuth2Client

from app import log
from app.core.config import settings
from app.core.exceptions import UnauthorizedError


class MyOAuth2Client(AsyncOAuth2Client):
    async def fetch_token(self, *args, **kwargs):
        # Disable SSL verification
        ssl_context = aiohttp.FakeSSLContext()

        # Modify the HTTP request to use the custom SSL context
        kwargs["ssl"] = ssl_context

        # Call the parent class's fetch_token method with the modified arguments
        return await super().fetch_token(*args, **kwargs)


class AuthHeader(TypedDict):
    Authorization: str


class AuthProvider:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: list[str] | None = None,
    ) -> None:
        self._token_url = token_url
        self._token_update_time: int | None = None

        self.custom_oauth_client = MyOAuth2Client(
            client_id=client_id, client_secret=client_secret, scope=scope
        )

        self.oauth_client = AsyncOAuth2Client(
            client_id=client_id, client_secret=client_secret, scope=scope, verify=False
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
            log.debug("The access_token or token_update_time attribute is None")
            return True

        else:
            time_elapsed = int(time.time()) - self.token_update_time
            log.debug(
                f"Token expiration info: token_update_time: {self.token_update_time}, "
                f"expires_in: {self.expires_in}, time_elapsed: {time_elapsed}"
            )
            return self.expires_in < (time_elapsed + 60)

    async def _fetch_access_token(self) -> None:
        log.debug("Fetching new access token")
        log.info("****************sathish*******************")
        log.info(self._token_url)
        try:
            await self.custom_oauth_client.fetch_token(
                url=self._token_url,
                grant_type="client_credentials",
            )
            self.token_update_time = int(time.time())

        except Exception as exc:
            log.error(f"An error occurred while fetching the access token: {exc}")

            raise UnauthorizedError("External API communication error")

    async def get_access_token(self, force_new: bool = False) -> str:
        with self.lock:
            if force_new or self.token_update_time is None:
                log.debug(f"Fetching new access token, {force_new=}")
                log.info(self._fetch_access_token())
                await self._fetch_access_token()
                log.info(self.access_token)

                return self.access_token

            if self._is_token_about_to_expire():
                log.debug("Token about to expire, fetching new access token")

                await self._fetch_access_token()

            return self.access_token


nc_auth = AuthProvider(
    client_id=settings.NC_CLIENT_ID,
    client_secret=settings.NC_CLIENT_SECRET,
    token_url=str(settings.NC_TOKEN_URL),
)

nc_reserve_auth = AuthProvider(
    client_id=settings.NC_CLIENT_ID,
    client_secret=settings.NC_CLIENT_SECRET,
    token_url=str(settings.NC_TOKEN_URL),
    scope=["55"],
)

nc_release_auth = AuthProvider(
    client_id=settings.NC_CLIENT_ID,
    client_secret=settings.NC_CLIENT_SECRET,
    token_url=str(settings.NC_TOKEN_URL),
    scope=["131"],
)

tinaa_auth = AuthProvider(
    client_id=settings.AUTH_CLIENT_ID,
    client_secret=settings.AUTH_CLIENT_SECRET,
    token_url=str(settings.AUTH_TOKEN_URL),
)
