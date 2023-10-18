from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
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
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation lists or finds Resource objects.
    """
    [column.strip() for column in fields.split(",")] if fields else None

    resources, total = await crud.reservation.get_multi(db=db, limit=limit, offset=offset)

    no_of_reservations = len(resources)

    log.info(f"Retrieved {no_of_reservations} Reservations(s)")
    log.info(f"Total available Reservations(s): {total}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([resource.to_schema() for resource in resources]),
        headers={"X-Result-Count": str(no_of_reservations), "X-Total-Count": str(total)},
    )


@router.post(
    "",
    summary="Creates a Reservation",
    responses=reservation_responses.create_responses,
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
    resource_create: Annotated[
        schemas.ReservationCreate, Body(description="The Resource to be created")
    ],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation creates a Resource entity.
    """
    resource = await crud.reservation.create(db=db, obj_in=resource_create)

    log.info(f"Created Resource with ID: {resource.id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(resource.to_schema()),
    )


@router.get(
    "/{id}",
    summary="Retrieves a Reservation by ID",
    responses=reservation_responses.get_responses,
    response_model=schemas.Reservation,
)
async def get_reservation_by_id(
    fields: Annotated[str, deps.FieldsQuery] = "",
    *,
    resource: Annotated[models.Reservation, Depends(deps.get_resource)],
) -> JSONResponse:
    """
    This operation retrieves a Resource entity. Attribute selection is enabled for all
    first level attributes.
    """
    log.info(f"{fields=}")

    log.info(f"Retrieved Resource with ID: {resource.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource.to_schema()),
    )


@router.delete(
    "/{id}",
    summary="Deletes a Resource",
    responses=reservation_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.Reservation, Depends(deps.get_resource)],
) -> Response:
    """
    This operation deletes a Resource entity.
    """
    await crud.reservation.delete(db=db, db_obj=resource)

    log.info(f"Deleted Resource with ID: {resource.id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{id}",
    summary="Updates partially a Resource",
    responses=reservation_responses.update_responses,
    response_model=schemas.Reservation,
)
async def update_resource_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.Reservation, Depends(deps.get_resource)],
    resource_update: Annotated[
        schemas.ReservationUpdate, Body(description="The Resource to be updated")
    ],
) -> JSONResponse:
    """
    This operation updates partially a Resource entity.
    """
    updated_resource = await crud.reservation.update(
        db=db, db_obj=resource, obj_in=resource_update
    )

    log.info(f"Updated Resource with ID: {updated_resource.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(updated_resource.to_schema()),
    )