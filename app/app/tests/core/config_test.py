import json
import os

import pytest
from pydantic import ValidationError

from app.core.config import Settings


class TestCORSOriginsSettings:
    def test_valid_cors_origins(self) -> None:
        origins = [
            "http://localhost/",
            "http://localhost:8050/",
            "http://localhost:8080/",
        ]

        os.environ["CORS_ORIGINS"] = json.dumps(origins)

        settings = Settings()  # type: ignore[call-arg]

        for input_origin, output_origin in zip(origins, settings.CORS_ORIGINS):
            assert input_origin == str(output_origin)

    def test_cors_origins_without_schema_raises_validation_error(self) -> None:
        origins = ["localhost:8050/"]

        os.environ["CORS_ORIGINS"] = json.dumps(origins)

        with pytest.raises(ValidationError):
            Settings()  # type: ignore[call-arg]


class TestDatabaseSettings:
    @pytest.fixture
    def set_db_config(self) -> str:
        username = "test_user"
        password = "test_password"
        host = "localhost"
        port = "3306"
        db_name = "db_name"

        os.environ["DB_USERNAME"] = username
        os.environ["DB_PASSWORD"] = password
        os.environ["DB_HOST"] = host
        os.environ["DB_PORT"] = port
        os.environ["DB_NAME"] = db_name

        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}"

    def test_sqlalchemy_uri_is_assembled(self, set_db_config: str) -> None:
        settings = Settings()  # type: ignore[call-arg]

        assert settings.DB_SQLALCHEMY_URI == set_db_config

    def test_sqlalchemy_uri_is_set_directly(self, set_db_config: str) -> None:
        sqlalchemy_uri = f"{set_db_config}_0"

        os.environ["DB_SQLALCHEMY_URI"] = sqlalchemy_uri

        settings = Settings()  # type: ignore[call-arg]

        assert settings.DB_SQLALCHEMY_URI == sqlalchemy_uri


class TestDebugSettings:
    @pytest.mark.parametrize("debug_value", ["True", "true", "1", "Yes", "yes"])
    def test_debug_is_boolean_true(self, debug_value: str) -> None:
        os.environ["DEBUG"] = debug_value

        settings = Settings()  # type: ignore[call-arg]

        assert settings.DEBUG is True

    @pytest.mark.parametrize("debug_value", ["False", "false", "0", "No", "no"])
    def test_no_debug_is_boolean_false(self, debug_value: str) -> None:
        os.environ["DEBUG"] = debug_value

        settings = Settings()  # type: ignore[call-arg]

        assert settings.DEBUG is False

    def test_debug_default_is_false(self) -> None:
        settings = Settings()  # type: ignore[call-arg]

        assert settings.DEBUG is False

    def test_debug_overwrites_log_level(self) -> None:
        os.environ["LOGGER_LEVEL"] = "WARNING"
        os.environ["DEBUG"] = "True"

        settings = Settings()  # type: ignore[call-arg]

        assert settings.LOGGER_LEVEL == "WARNING"

    def test_no_debug_leaves_log_level(self) -> None:
        os.environ["LOGGER_LEVEL"] = "WARNING"
        os.environ["DEBUG"] = "False"

        settings = Settings()  # type: ignore[call-arg]

        assert settings.LOGGER_LEVEL == "WARNING"


class TestLoggerLevelSettings:
    @pytest.mark.parametrize(
        "logger_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )
    def test_valid_logger_levels(self, logger_level: str) -> None:
        os.environ["LOGGER_LEVEL"] = logger_level

        settings = Settings()  # type: ignore[call-arg]

        assert settings.LOGGER_LEVEL == logger_level

    @pytest.mark.parametrize("logger_level", ["TRACE", "INFORMATION", "WARN", "FATAL"])
    def test_invalid_logger_levels_raise_validation_error(
        self, logger_level: str
    ) -> None:
        os.environ["LOGGER_LEVEL"] = logger_level

        with pytest.raises(ValidationError):
            Settings()  # type: ignore[call-arg]

    def test_default_logger_level_is_info(self) -> None:
        settings = Settings()  # type: ignore[call-arg]

        assert settings.LOGGER_LEVEL == "INFO"
