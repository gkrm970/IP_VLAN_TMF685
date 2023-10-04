from fastapi import APIRouter

from .endpoints.reservation_endpoints import router as reservation_router
from .endpoints.resource_endpoints import router as resource_router

router = APIRouter()
router.include_router(resource_router, prefix="/resource/pool", tags=["resource pool"])
router.include_router(reservation_router, prefix="/reservation/pool", tags=["reservation pool"])

