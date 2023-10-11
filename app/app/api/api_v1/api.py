from fastapi import APIRouter

from .endpoints.reservation_endpoints import router as reservation_router

router = APIRouter()
router.include_router(
    reservation_router, prefix="/reservation", tags=["Reservation"]
)
<<<<<<< Updated upstream
=======
router.include_router(
    resource_pool_router, prefix="/resource", tags=["Resource"]
)
>>>>>>> Stashed changes
