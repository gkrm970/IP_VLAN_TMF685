import json
import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings


def test_create_resource(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    test_request_payload = {"name": "test_name"}

    async def mock_create(
        db: AsyncSession, obj_in: schemas.ResourceCreate
    ) -> models.Resource:
        db_obj_id = uuid.uuid4().hex

        return models.Resource(
            name="test_name", id=db_obj_id, href=f"resource/{db_obj_id}"
        )

    monkeypatch.setattr(crud.resource, "create", mock_create)

    response = client.post(
        f"{settings.API_PREFIX}/resource",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "test_name"
