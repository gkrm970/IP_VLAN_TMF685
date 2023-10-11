from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, schemas, models
from app.api import deps
from app.api.responses import reservation_responses
import json

# # Open the JSON file in read mode
# with open(
#         'D:\\Telus\TMF-685\\tmf685-resource-pool-management\\app\\app\json_files\\resource_service_inventory_638.json',
#         'r') as json_file:
#     # Load JSON data from the file
#     resource_specification = json.load(json_file)

router = APIRouter()


@router.post(
    "",
    summary="Creates a Resource Pool",
    responses=reservation_responses.create_responses,
    response_model=schemas.ResourceSpecificationCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource_pool(
        resource_create: Annotated[schemas.ResourceSpecificationCreate,
        Body(description="The Resource pool to be created"),
        ],
        db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation creates a Resource pool entity.
    """

    resource_pool = await crud.resource_pool.create(db=db, obj_in=resource_create)

    # Exclude unset does not work on simply the resource.to_dict, because the DB model
    # contains even the default/nulled properties. We need to build an include set from
    # the resource create schema - the only time we can actually know what was not set

    log.critical(resource_create.model_dump(exclude_unset=True))

    log.info(f"Created Resource pool with ID: {resource_pool.id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource_pool.to_dict()),  # type: ignore
    )


@router.get(
    "",
    summary="Retrieves a list of Resource Pools",
    responses=reservation_responses.get_responses,
    response_model=list[schemas.ResourceSpecification],
    status_code=status.HTTP_200_OK,
)
async def get_resource_pool(
        fields: Annotated[str, deps.FieldsQuery] = "",
        offset: Annotated[int, deps.OffsetQuery] = 0,
        limit: Annotated[int, deps.LimitQuery] = 100,
        *,
        db: Annotated[AsyncSession, Depends(deps.get_db_session)]
) -> JSONResponse:
    """
    This operation retrieves a list of Resource Pools.
    """
    resource, total = await crud.resource_pool.get_multi(
        db=db, limit=limit, offset=offset)
    no_of_resource_pool = len(resource)

    log.info(f"Retrieved {no_of_resource_pool} Resource pool(s)")
    log.info(f"Total available Resource(s): {total}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder([resource.to_dict() for resource in resource]),
        headers={"X-Result-Count": str(no_of_resource_pool), "X-Total-Count": str(total)}
    )


@router.get(
    "/{id}",
    summary="Retrieves a Resource Pool by ID",
    responses=reservation_responses.get_responses,
    response_model=schemas.ResourceSpecification,
    status_code=status.HTTP_200_OK,
)
async def get_resource_pool_by_id(
        id: str,
        fields: Annotated[str, deps.FieldsQuery] = "",
        *,
        db: Annotated[AsyncSession, Depends(deps.get_db_session)]
) -> JSONResponse:
    """
    This operation retrieves a Resource Pool by ID.
    """
    resource = await crud.resource_pool.get(db=db, id=id)
    log.info(f"Retrieved Resource pool with ID: {resource.id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource.to_dict())
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
        resource: Annotated[models.ResourceSpecification, Depends(deps.get_resource)],
):
    """
    This operation deletes a Resource Pool by ID.
    """
    await crud.resource_pool.delete(db=db, db_obj=resource)
    log.info(f"Deleted Resource pool with ID: {resource.id}")
    return "Resource record deleted successfully"


@router.patch(
    "/{id}",
    summary="Updates partially a Resource Pool by ID",
    responses=reservation_responses.update_responses,
    response_model=schemas.ResourceSpecification,
)
async def update_resource_pool_by_id(
        id: str,
        resource_update: Annotated[schemas.ResourceSpecificationUpdate,
        Body(description="The Resource pool to be updated")],
        db_obj: Annotated[models.ResourceSpecification, Depends(deps.get_resource)],
        *,
        db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> JSONResponse:
    """
    This operation updates partially a Resource Pool by ID.
    """
    resource = await crud.resource_pool.update(db=db, id=id, obj_in=resource_update,db_obj=db_obj)
    log.info(f"Updated Resource pool with ID: {resource.id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(resource.to_dict())
    )
