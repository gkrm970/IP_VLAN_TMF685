from fastapi.routing import APIRouter

from app.api.api_v1.endpoints import (
    items,
    utils,
)

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])


