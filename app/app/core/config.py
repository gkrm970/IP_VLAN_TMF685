from typing import Literal, TypeAlias

from pydantic import AnyHttpUrl, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class APISettings(BaseSettings):
    API_NAME: str = "plan/resourcePoolManagement"
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/{API_NAME}/{API_VERSION}"


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "root"
    DB_HOST: str = "10.17.36.156"
    DB_PORT: int = 3306
    DB_NAME: str = "reservation_db"
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

        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}"


class LoggerSettings(BaseSettings):
    LOGGER_NAME: str = "Resource Pool Management"
    LOGGER_LEVEL: LogLevel = "INFO"
    LOGGER_FORMAT: str = (
        "[%(asctime)s] [%(levelname)s] [%(name)s] "
        "[PID %(process)d] [TID %(thread)d] [X-ID %(correlation_id)s] "
        "[%(filename)s.%(lineno)s -> %(funcName)s()] %(message)s"
    )
    LOGGER_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"


class Settings(APISettings, DatabaseSettings, LoggerSettings):
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
