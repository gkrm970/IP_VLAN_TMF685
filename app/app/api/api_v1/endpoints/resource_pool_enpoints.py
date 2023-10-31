from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, schemas, models
from app.api import deps
from app.api.responses import reservation_responses
from app.api.utils.resource_pool_alias_mapping import get_include_fields_for_response

router = APIRouter()


@router.post(
    "",
    summary="Creates a Resource Pool",
    responses=reservation_responses.create_responses,
    response_model=schemas.ResourcePoolManagementCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource_pool(
    resource_create: Annotated[
        schemas.ResourcePoolManagementCreate,
        Body(description="The Resource pool to be created"),
    ],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation creates a Resource pool entity.
    """

    resource_pool = await crud.resource_pool.create(db, resource_create)

    # Exclude unset does not work on simply the resource.to_dict, because the DB model
    # contains even the default/nulled properties. We need to build an include set from
    # the resource create schema - the only time we can actually know what was not set

    log.critical(resource_create.model_dump(exclude_unset=True))

    log.info(f"Created Resource pool with ID: {resource_pool.id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(resource_pool.to_dict()),
    )


@router.get(
    "",
    summary="Retrieves a list of Resource Pools",
    responses=reservation_responses.get_responses,
    response_model=list[schemas.ResourcePoolManagement],
    status_code=status.HTTP_200_OK,
)
async def get_resource_pools(
    fields: Annotated[str, deps.FieldsQuery] = "",
    offset: Annotated[int, deps.OffsetQuery] = 0,
    limit: Annotated[int, deps.LimitQuery] = 100,
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation retrieves a list of Resource Pools.
    """
    include = get_include_fields_for_response(fields)
    resource, total = await crud.resource_pool.get_multi(db, limit, offset)
    no_of_resource_pool = len(resource)

    log.info(f"Retrieved {no_of_resource_pool} Resource pool(s)")
    log.info(f"Total available Resource(s): {total}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            [resource.to_dict(include=include) for resource in resource]
        ),
        headers={
            "X-Result-Count": str(no_of_resource_pool),
            "X-Total-Count": str(total),
        },
    )


@router.get(
    "/{id}",
    summary="Retrieves a Resource Pool by ID",
    responses=reservation_responses.get_responses,
    response_model=schemas.ResourcePoolManagementCreate,
    status_code=status.HTTP_200_OK,
)
async def get_resource_pool_by_id(
    fields: Annotated[str, deps.FieldsQuery] = "",
    *,
    resource_pool: Annotated[models.ResourcePoolManagement, Depends(deps.get_resource)],
) -> JSONResponse:
    """
    This operation retrieves a Resource Pool by ID.
    """
    include = get_include_fields_for_response(fields)

    log.info(f"Retrieved Resource pool with ID: {resource_pool.id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource_pool.to_dict(include=include)),
    )


@router.delete(
    "/{id}",
    summary="Deletes a Resource Pool by ID",
    responses=reservation_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource_pool_by_id(
    id: str,
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.ResourcePoolManagement, Depends(deps.get_resource)],
) -> Response:
    """
    This operation deletes a Resource Pool by ID.
    """
    await crud.resource_pool.delete(db, resource)

    log.info(f"Deleted Resource Pool with ID: {resource.id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{id}",
    summary="Updates partially a Resource Pool by ID",
    responses=reservation_responses.update_responses,
    response_model=schemas.ResourcePoolManagementUpdate,
)
async def update_resource_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.ResourcePoolManagement, Depends(deps.get_resource)],
    resource_update: Annotated[
        schemas.ResourcePoolManagementUpdate,
        Body(description="The Resource Pool to be updated"),
    ],
) -> JSONResponse:
    """
    This operation updates partially a Resource entity.
    """
    updated_resource = await crud.resource_pool.update(db, resource, resource_update)

    log.info(f"Updated Resource Pool ID: {updated_resource.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(updated_resource.to_dict()),
    )
