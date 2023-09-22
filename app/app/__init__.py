import logging
import sys

from asgi_correlation_id import CorrelationIdFilter

from app.core.config import settings


def create_app_logger() -> logging.Logger:
    app_logger = logging.getLogger(settings.LOGGER_NAME)
    app_logger.setLevel(settings.LOGGER_LEVEL)
    app_logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt=settings.LOGGER_FORMAT, datefmt=settings.LOGGER_DATE_FORMAT
        )
    )
    handler.setLevel(settings.LOGGER_LEVEL)
    handler.addFilter(CorrelationIdFilter(uuid_length=32, default_value="-"))

    app_logger.addHandler(handler)

    # Intercept uvicorn logs
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = app_logger.handlers
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = app_logger.handlers

    return app_logger


log = create_app_logger()
