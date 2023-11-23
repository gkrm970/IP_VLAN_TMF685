from asgi_correlation_id.middleware import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_TITLE,
    docs_url=f"{settings.API_PREFIX}/docs",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["X-Request-ID"],
    expose_headers=[
        "X-Request-ID",  # From the CorrelationIdMiddleware for logging purposes
        "X-Result-Count",  # Response header, actual number of items returned
        "X-Total-Count",  # Response header, total number of items matching criteria
    ],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/", include_in_schema=False)
async def redirect() -> RedirectResponse:
    response = RedirectResponse(url=f"{settings.API_PREFIX}/docs")
    return response
