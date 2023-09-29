from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.api import deps


async def get_resource(
    id: Annotated[str, Path(description="Identifier of the Resource")],
    db: Annotated[AsyncSession, Depends(deps.get_db_session)],
) -> models.Resource:
    resource = await crud.resource.get(db=db, id=id)

    if resource is None:
        raise HTTPException(
            detail=f"No resource found with ID {id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return resource
