from typing import Annotated

from fastapi import APIRouter, Body, Depends, status, Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, models, schemas
from app.api import deps
from app.api.responses import reservation_responses
from app.core import security
from app.schemas import TokenPayload

router = APIRouter(dependencies=[Security(deps.validate_token_signature)])


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
    current_user: TokenPayload = Depends(
        security.ValidateAccessRoles(["uinv:tmf685:reservation:ro"])
    ),
) -> JSONResponse:
    """
    This operation lists or finds Resource objects.
    """
    [column.strip() for column in fields.split(",")] if fields else None

    resources, total = await crud.reservation.get_multi(db, limit, offset)

    no_of_reservations = len(resources)

    log.info(f"Retrieved {no_of_reservations} Reservations(s)")
    log.info(f"Total available Reservations(s): {total}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([resource.to_dict() for resource in resources]),
        headers={
            "X-Result-Count": str(no_of_reservations),
            "X-Total-Count": str(total),
        },
    )


@router.post(
    "",
    summary="Creates a Reservation",
    responses=reservation_responses.create_responses,
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
    reservation_create: Annotated[
        schemas.ReservationCreate, Body(description="The Reservation to be created")
    ],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    current_user: TokenPayload = Depends(
        security.ValidateAccessRoles(["uinv:tmf685:reservation:rw"])
    ),
) -> JSONResponse:
    """
    This operation creates a Reservation entity.
    """

    reservation = await crud.reservation.create(db, reservation_create)

    log.info(f"Created Reservation with ID: {reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(reservation.to_dict()),
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
    resource: Annotated[models.Reservation, Depends(deps.get_reservation)],
    current_user: TokenPayload = Depends(
        security.ValidateAccessRoles(["uinv:tmf685:reservation:ro"])
    ),
) -> JSONResponse:
    """
    This operation retrieves a Resource entity. Attribute selection is enabled for all
    first level attributes.
    """
    log.info(f"{fields=}")

    log.info(f"Retrieved Resource with ID: {resource.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource.to_dict()),
    )


@router.delete(
    "/{id}",
    summary="Deletes a Reservation by ID",
    responses=reservation_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reservation_by_id(
    id: str,
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
    current_user: TokenPayload = Depends(
        security.ValidateAccessRoles(["uinv:tmf685:reservation:rw"])
    ),
) -> Response:
    """
    This operation deletes a Reservation by ID.
    """
    await crud.reservation.delete(db, reservation)

    log.info(f"Deleted Reservation with ID: {reservation.id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{id}",
    summary="Updates partially a Reservation by ID",
    responses=reservation_responses.update_responses,
    response_model=schemas.ReservationUpdate,
)
async def update_reservation_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    reservation: Annotated[models.Reservation, Depends(deps.get_reservation)],
    reservation_update: Annotated[
        schemas.ReservationUpdate, Body(description="The Reservation to be updated")
    ],
    current_user: TokenPayload = Depends(
        security.ValidateAccessRoles(["uinv:tmf685:reservation:rw"])
    ),
) -> JSONResponse:
    """
    This operation updates partially a Reservation entity.
    """
    update_reservation = await crud.reservation.update(
        db, reservation, reservation_update
    )

    log.info(f"Updated Reservation ID: {update_reservation.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(update_reservation.to_dict()),
    )
