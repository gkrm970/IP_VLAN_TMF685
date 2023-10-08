import json
import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings


class TestCreateResource:
    @staticmethod
    async def _mock_create(
        db: AsyncSession, obj_in: schemas.ReservationCreate
    ) -> models.Reservation:
        db_obj_id = uuid.uuid4().hex

        return models.Reservation(
            name="test_name", id=db_obj_id, href=f"reservation/{db_obj_id}"
        )

    def test_create_resource_ok(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        test_request_payload = {"name": "test_name"}

        monkeypatch.setattr(crud.reservation, "create", self._mock_create)

        response = client.post(
            f"{settings.API_PREFIX}/resource",
            content=json.dumps(test_request_payload),
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "test_name"

    def test_create_resource_missing_name(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        test_request_payload = {"category": "test_category"}

        monkeypatch.setattr(crud.reservation, "create", self._mock_create)

        response = client.post(
            f"{settings.API_PREFIX}/resource",
            content=json.dumps(test_request_payload),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
