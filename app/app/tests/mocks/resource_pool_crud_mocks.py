import random
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas

_existing_resource_id = str(uuid.uuid4())

EXISTING_RESOURCE = models.ResourcePool(
    name="test_name",
    id=_existing_resource_id,
    href=f"resourcePool/{_existing_resource_id}",
)


async def get_multi(
    _db: AsyncSession,
    _limit: int = 100,
    _offset: int = 0,
) -> tuple[list[models.ResourcePool], int]:
    resources = []
    number_of_resources = random.randint(1, 10)

    for _ in range(number_of_resources):
        db_obj_id = str(uuid.uuid4())

        resources.append(
            models.ResourcePool(
                name="test_name",
                id=db_obj_id,
                href=f"resourcePool/{db_obj_id}",
                type="test",
            )
        )

    return resources, number_of_resources


async def create(
    _db: AsyncSession, _obj_in: schemas.ResourcePoolCreate
) -> models.ResourcePool:
    db_obj_id = str(uuid.uuid4())

    return models.ResourcePool(
        name="test_name", id=db_obj_id, href=f"resourcePool/{db_obj_id}"
    )


async def get(_db: AsyncSession, id: str) -> models.ResourcePool | None:
    if id == EXISTING_RESOURCE.id:
        return EXISTING_RESOURCE

    return None


async def delete(_db: AsyncSession, _db_obj: models.ResourcePool) -> None:
    return None


async def update(_db: AsyncSession, _db_obj: models.ResourcePool) -> None:
    return None
