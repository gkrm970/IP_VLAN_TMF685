from fastapi import APIRouter

from .endpoints.reservation_endpoints import router as reservation_router

router = APIRouter()
router.include_router(
    reservation_router, prefix="/reservation/pool", tags=["reservation pool"]
)
