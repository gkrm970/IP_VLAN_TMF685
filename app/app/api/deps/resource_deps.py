from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.api import deps
from app.core.exceptions import NotFoundError


async def get_resource(
    id: Annotated[str, Path(description="Identifier of the Resource pool")],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> models.ResourcePool:
    resource = await crud.resource_pool.get(db, id)

    if resource is None:
        raise NotFoundError(f"No resource pool found with ID {id}")
    return resource


async def get_reservation(
    id: Annotated[str, Path(description="Identifier of the Reservation")],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> models.Reservation:
    reservation = await crud.reservation.get(db, id)

    if reservation is None:
        raise NotFoundError(f"No reservation found with ID {id}")
    return reservation
