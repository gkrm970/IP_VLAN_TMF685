from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, models, schemas
from app.api import deps
from app.api.responses import reservation_responses

router = APIRouter()


@router.get(
    "",
    summary="Lists or finds Reservation objects",
    responses=reservation_responses.get_responses,
    response_model=list[schemas.Reservation],
)
async def get_reservations(
        fields: Annotated[str, deps.FieldsQuery] = "",
        offset: Annotated[int, deps.OffsetQuery] = 0,
        limit: Annotated[int, deps.LimitQuery] = 100,
        *,
        db: Annotated[AsyncSession, Depends(deps.get_db_session)]
) -> JSONResponse:
    """
    This operation lists or finds Reservation objects.
    """
    include = deps.get_include_fields(fields)

    reservation, total = await crud.reservation.get_multi(
        db=db, limit=limit, offset=offset
    )

    no_of_reservation_pool = len(reservation)

    log.info(f"Retrieved {no_of_reservation_pool} Reservation pool(s)")
    log.info(f"Total available Reservation(s): {total}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([reservation.to_dict(include_fields=include) for reservation in reservation]),
        headers={"X-Result-Count": str(no_of_reservation_pool), "X-Total-Count": str(total)})


@router.post(
    "",
    summary="Creates a Reservation",
    responses=reservation_responses.create_responses,
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
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

    # Exclude unset does not work on simply the resource.to_schema, because the DB model
    # contains even the default/nulled properties. We need to build an include set from
    # the resource create schema - the only time we can actually know what was not set

    log.critical(reservation_create.model_dump(exclude_unset=True))

    log.info(f"Created Reservation pool with ID: {reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(reservation.to_dict()),  # type: ignore
    )


@router.get(
    "/{id}",
    summary="Retrieves a Reservation by ID",
    responses=reservation_responses.get_responses,
    response_model=schemas.Reservation,
)
async def get_reservation_pool_by_id(
        fields: Annotated[str, deps.FieldsQuery] = "",
        *,
        reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
) -> JSONResponse:
    """
    This operation retrieves a Reservation entity. Attribute selection is enabled for all
    first level attributes.
    """
    include = deps.get_include_fields(fields)

    log.info(f"{fields=}")

    log.info(f"Retrieved Reservation with ID: {reservation.id}")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(reservation.to_dict(include_fields=include))
                        )


@router.delete(
    "/{id}",
    summary="Deletes a Reservation by ID",
    responses=reservation_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reservation_pool_by_id(
        db: Annotated[AsyncSession, Depends(deps.get_db_session)],
        reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
):
    """
    This operation deletes a Reservation entity.
    """
    await crud.reservation.delete(db=db, db_obj=reservation)

    log.info(f"Deleted Reservation with ID: {reservation.id}")


@router.patch(
    "/{id}",
    summary="Updates partially a Reservation by ID",
    responses=reservation_responses.update_responses,
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
    This operation updates partially a Reservation entity.
    """
    updated_reservation = await crud.reservation.update(
        db=db, db_obj=db_se, obj_in=reservation_update
    )

    log.info(f"Updated Reservation with ID: {updated_reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(updated_reservation.to_dict()),
    )
