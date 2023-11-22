from typing import Any, Literal, TypeAlias
from urllib.parse import urljoin

from pydantic import AnyHttpUrl, Json, ValidationInfo, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

JWKSet: TypeAlias = dict[str, list[dict[str, Any]]]


class APISettings(BaseSettings):
    API_BASE_URL: AnyHttpUrl
    API_NAME: str = "resourcePoolManagement"
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/{API_NAME}/{API_VERSION}"


class AuthSettings(BaseSettings):
    AUTH_BASE_URL: AnyHttpUrl
    AUTH_AUTHORIZATION_URL: AnyHttpUrl | None = None
    AUTH_JWK_SET_URL: AnyHttpUrl | None = None
    AUTH_TOKEN_URL: AnyHttpUrl | None = None
    SSL_VERIFY: Any = False
    # This will be set after application startup, getting it from the JWK_SET_URL above
    AUTH_JWK_SET: Json[JWKSet] | None = None

    AUTH_CLIENT_ID: str
    AUTH_CLIENT_SECRET: str

    @field_validator("AUTH_AUTHORIZATION_URL", mode="before")
    def assemble_authorization_url(
        cls, field: AnyHttpUrl | None, field_info: ValidationInfo  # noqa: N805
    ) -> AnyHttpUrl:
        if field is not None:
            return field

        base_url = str(field_info.data.get("AUTH_BASE_URL"))

        return Url(urljoin(f"{base_url}/", "auth"))

    @field_validator("AUTH_JWK_SET_URL", mode="before")
    def assemble_jwk_set_url(
        cls, field: AnyHttpUrl | None, field_info: ValidationInfo  # noqa: N805
    ) -> AnyHttpUrl:
        if field is not None:
            return field

        base_url = str(field_info.data.get("AUTH_BASE_URL"))

        return Url(urljoin(f"{base_url}/", "certs"))

    @field_validator("AUTH_TOKEN_URL", mode="before")
    def assemble_token_url(
        cls, field: AnyHttpUrl | None, field_info: ValidationInfo  # noqa: N805
    ) -> AnyHttpUrl:
        if field is not None:
            return field

        base_url = str(field_info.data.get("AUTH_BASE_URL"))

        return Url(urljoin(f"{base_url}/", "token"))


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_SQLALCHEMY_URI: str | None = None

    @field_validator("DB_SQLALCHEMY_URI", mode="before")
    def assemble_db_sqlalchemy_uri(
        cls, field: str | None, field_info: ValidationInfo  # noqa: N805
    ) -> str:
        if isinstance(field, str):
            return field

        username = field_info.data.get("DB_USERNAME")
        password = field_info.data.get("DB_PASSWORD")
        host = field_info.data.get("DB_HOST")
        port = field_info.data.get("DB_PORT")
        db_name = field_info.data.get("DB_NAME")

        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"


class LoggerSettings(BaseSettings):
    LOGGER_NAME: str = "Resource Pool Management"
    LOGGER_LEVEL: LogLevel = "INFO"
    LOGGER_FORMAT: str = (
        "[%(asctime)s] [%(levelname)s] [%(name)s] "
        "[PID %(process)d] [TID %(thread)d] [X-ID %(correlation_id)s] "
        "[%(filename)s.%(lineno)s -> %(funcName)s()] %(message)s"
    )
    LOGGER_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"


class NetCrackerProviderSettings(BaseSettings):
    NC_CLIENT_ID: str
    NC_CLIENT_SECRET: str
    NC_TOKEN_URL: AnyHttpUrl
    NC_API_BASE_URL: str


class ResourceInventoryProviderSettings(BaseSettings):
    RI_PROVIDER_BASE_URL: str = "http://127.0.0.1:8000"
    API_NAME: str = "plan/inventory/resourceInventoryManagement"
    API_VERSION: str = "v1"
    RI_PROVIDER_API_PREFIX: str = f"/{API_NAME}/{API_VERSION}"


class Settings(
    AuthSettings,
    APISettings,
    DatabaseSettings,
    LoggerSettings,
    ResourceInventoryProviderSettings,
):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
    )

    PROJECT_NAME: str = "Resource Pool Management"

    # CORS_ORIGINS is a JSON-formatted list of origins (HTTP URLs),
    # e.g: '["http://localhost", "http://localhost:8050", "http://localhost:8080"]'
    CORS_ORIGINS: list[AnyHttpUrl] = []

    DEBUG: bool = False


settings = Settings()  # type: ignore[call-arg]
