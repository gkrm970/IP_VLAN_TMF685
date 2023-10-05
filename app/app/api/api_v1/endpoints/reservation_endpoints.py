from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, models, schemas
from app.api import deps
from app.api.responses import resource_responses

router = APIRouter()


@router.get(
    "",
    summary="Lists or finds Reservation Pool objects",
    responses=resource_responses.get_responses,
    response_model=list[schemas.Reservation],
)
async def get_reservation(
    fields: Annotated[str, deps.FieldsQuery] = "",
    offset: Annotated[int, deps.OffsetQuery] = 0,
    limit: Annotated[int, deps.LimitQuery] = 100,
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    response: Response,
) -> list[models.Reservation]:
    """
    This operation lists or finds Reservation objects.
    """
    reservation, total = await crud.reservation.get_multi(
        db=db, limit=limit, offset=offset
    )

    no_of_reservation_pool = len(reservation)

    log.info(f"Retrieved {no_of_reservation_pool} Reservation pool(s)")
    log.info(f"Total available Reservation pool(s): {total}")

    response.headers["X-Result-Count"] = str(no_of_reservation_pool)
    response.headers["X-Total-Count"] = str(total)

    return reservation


@router.post(
    "",
    summary="Creates a Reservation pool",
    responses=resource_responses.create_responses,
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation_pool(
    reservation_create: Annotated[
        schemas.ReservationCreate,
        Body(description="The Reservation pool to be created"),
    ],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation creates a Reservation pool entity.
    """
    reservation = await crud.reservation.create(db=db, obj_in=reservation_create)

    log.info(f"Created Reservation pool with ID: {reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(reservation.to_schema()),  # type: ignore
    )


@router.get(
    "/{id}",
    summary="Retrieves a Reservation pool by ID",
    responses=resource_responses.get_responses,
    response_model=schemas.Reservation,
)
async def get_reservation_pool_by_id(
    fields: Annotated[str, deps.FieldsQuery] = "",
    *,
    reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
) -> models.Reservation:
    """
    This operation retrieves a Reservation pool entity. Attribute selection is enabled for all
    first level attributes.
    """
    log.info(f"{fields=}")

    log.info(f"Retrieved Reservation pool with ID: {reservation.id}")

    return reservation


@router.delete(
    "/{id}",
    summary="Deletes a Reservation pool",
    responses=resource_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reservation_pool_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
) -> None:
    """
    This operation deletes a Reservation pool entity.
    """
    await crud.reservation.delete(db=db, db_obj=reservation)

    log.info(f"Deleted Reservation pool with ID: {reservation.id}")


@router.patch(
    "/{id}",
    summary="Updates partially a Reservation pool",
    responses=resource_responses.update_responses,
    response_model=schemas.Reservation,
)
async def update_reservation_pool_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    db_se: Annotated[models.Reservation, Depends(deps.get_reservation)],
    reservation_update: Annotated[
        schemas.ReservationUpdate,
        Body(description="The Reservation pool to be updated"),
    ],
) -> JSONResponse:
    """
    This operation updates partially a Reservation pool entity.
    """
    updated_reservation = await crud.reservation.update(
        db=db, db_obj=db_se, obj_in=reservation_update
    )

    log.info(f"Updated Reservation pool with ID: {updated_reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(updated_reservation.to_schema()),
    )
