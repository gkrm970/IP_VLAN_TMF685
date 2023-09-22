import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator
from starlette.middleware import Middleware
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins


class Settings(BaseSettings):

    DOMAIN: str = "localhost"
    VERSION: str = "1.0.0"
    API_VERSION:str = "v1"
    API_NAME: str = "tmf-tinaa"
    API_VERSION_STR: str = f"/{API_NAME}/" + API_VERSION

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if v is None or len(v) == 0:
            return None
        return v


    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


    MIDDLEWARES: list = [
        Middleware(
            ContextMiddleware,
            plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
        )
    ]

    AUTH_AUTHORIZATION_URL: AnyHttpUrl
    AUTH_TOKEN_URL: AnyHttpUrl
    AUTH_REDIRECT_URL: str = "/docs"


    LOGGER_APP_NAME: str = "COOKIECUTTER"
    LOGGER_APP_CODE: str = "0098"
    LOGGER_HANDLER_NAME = "console"
    TINAA_LOG_LEVEL: str
    LOGGER_FORMAT = "[%(asctime)s] [%(levelname)s] [{}] [{}] [%(filename)s -> %(funcName)s()] [%(lineno)s] %(message)s"
    LOGGER_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    class Config:
        case_sensitive = True


settings = Settings()       # type: ignore