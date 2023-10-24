from fastapi import APIRouter

from .endpoints.reservation_endpoints import router as reservation_router
from .endpoints.resource_pool_enpoints import router as resource_pool_router

router = APIRouter()
router.include_router(reservation_router, prefix="/reservation", tags=["Reservation"])
router.include_router(resource_pool_router, prefix="/resourcePool", tags=["ResourcePool"])
