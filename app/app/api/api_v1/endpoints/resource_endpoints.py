from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, log, models, schemas
from app.api import deps
from app.api.responses import resource_responses

router = APIRouter()


@router.get(
    "",
    summary="Lists or finds Resource objects",
    responses=resource_responses.get_responses,
    response_model=list[schemas.Resource],
)
async def get_resources(
    fields: Annotated[str, deps.FieldsQuery] = "",
    offset: Annotated[int, deps.OffsetQuery] = 0,
    limit: Annotated[int, deps.LimitQuery] = 100,
    *,
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    response: Response,
) -> list[models.Resource]:
    """
    This operation lists or finds Resource objects.
    """
    resources, total = await crud.resource.get_multi(db=db, limit=limit, offset=offset)

    no_of_resource = len(resources)

    log.info(f"Retrieved {no_of_resource} Resource(s)")
    log.info(f"Total available Resource(s): {total}")

    response.headers["X-Result-Count"] = str(no_of_resource)
    response.headers["X-Total-Count"] = str(total)

    return resources


@router.post(
    "",
    summary="Creates a Resource",
    responses=resource_responses.create_responses,
    response_model=schemas.Resource,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    resource_create: Annotated[
        schemas.ResourceCreate, Body(description="The Resource to be created")
    ],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> models.Resource:
    """
    This operation creates a Resource entity.
    """
    resource = await crud.resource.create(db=db, obj_in=resource_create)

    log.info(f"Created Resource with ID: {resource.id}")

    return resource


@router.get(
    "/{id}",
    summary="Retrieves a Resource by ID",
    responses=resource_responses.get_responses,
    response_model=schemas.Resource,
)
async def get_resource_by_id(
    fields: Annotated[str, deps.FieldsQuery] = "",
    *,
    resource: Annotated[models.Resource, Depends(deps.get_resource)],
) -> models.Resource:
    """
    This operation retrieves a Resource entity. Attribute selection is enabled for all
    first level attributes.
    """
    log.info(f"{fields=}")

    log.info(f"Retrieved Resource with ID: {resource.id}")

    return resource


@router.delete(
    "/{id}",
    summary="Deletes a Resource",
    responses=resource_responses.delete_responses,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.Resource, Depends(deps.get_resource)],
) -> None:
    """
    This operation deletes a Resource entity.
    """
    await crud.resource.delete(db=db, db_obj=resource)

    log.info(f"Deleted Resource with ID: {resource.id}")


@router.patch(
    "/{id}",
    summary="Updates partially a Resource",
    responses=resource_responses.update_responses,
    response_model=schemas.Resource,
)
async def update_resource_by_id(
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
    resource: Annotated[models.Resource, Depends(deps.get_resource)],
    resource_update: Annotated[
        schemas.ResourceUpdate, Body(description="The Resource to be updated")
    ],
) -> models.Resource:
    """
    This operation updates partially a Resource entity.
    """
    updated_resource = await crud.resource.update(
        db=db, db_obj=resource, obj_in=resource_update
    )

    log.info(f"Updated Resource with ID: {updated_resource.id}")

    return updated_resource
