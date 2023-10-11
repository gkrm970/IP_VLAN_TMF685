from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.api import deps


async def get_resource(
    id: Annotated[str, Path(description="Identifier of the Resource pool")],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> models.ResourceSpecification:
    resource = await crud.resource_pool.get(db=db, id=id)

    if resource is None:
        raise HTTPException(
            detail=f"No Resource pool record found with ID {id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return resource

