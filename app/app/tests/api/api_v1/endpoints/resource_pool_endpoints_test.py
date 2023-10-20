import json
import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings
from app.tests.mocks import resource_pool_crud_mocks as mocks


class TestGetResourcesPool:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_get_multi(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "get_multi", mocks.get_multi)

    def test_get_resources_pool_status_code_is_200(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/resourcePool")

        assert response.status_code == status.HTTP_200_OK

    def test_get_resources_responds_with_list_of_resources(
            self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/resourcePool")

        assert isinstance(response.json(), list)

        for resource in response.json():
            assert resource["name"] == "test_name"

    def test_get_resources_pool_responds_with_defined_query_fields(
            self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool", params={"fields": "name"}
        )

        for resource in response.json():
            assert "category" not in resource

    def test_get_resources_pool_responds_with_mandatory_fields_always(
            self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool", params={"fields": "name"}
        )

        for resource in response.json():
            assert "id" in resource
            assert "href" in resource
            assert "name" in resource

    def test_get_resources_responds_with_x_total_count_header(
            self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/resourcePool")

        assert "X-Total-Count" in response.headers

    def test_get_resources_pool_responds_with_x_result_count_header(
            self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/resourcePool")

        assert "X-Result-Count" in response.headers


class TestCreateResourcePool:
    @staticmethod
    async def _mock_create(
            db: AsyncSession, obj_in: schemas.ResourcePoolManagementCreate
    ) -> models.ResourcePoolManagement:
        db_obj_id = uuid.uuid4().hex

        return models.ResourcePoolManagement(
            name="test_name", id=db_obj_id, href=f"resourcePool/{db_obj_id}"
        )

    def test_create_resource_pool_status_code_is_201(
            self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        test_request_payload = {"name": "test_name"}

        monkeypatch.setattr(crud.resource_pool, "create", self._mock_create)

        response = client.post(
            f"{settings.API_PREFIX}/resourcePool",
            content=json.dumps(test_request_payload),
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "test_name"

    def test_create_resource_missing_name(
            self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        test_request_payload = {"category": "test_category"}

        monkeypatch.setattr(crud.resource_pool, "create", self._mock_create)

        response = client.post(
            f"{settings.API_PREFIX}/resourcePool",
            content=json.dumps(test_request_payload),
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetResourcePoolByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "get", mocks.get)

    def test_get_resource_pool_by_id_status_code_is_200(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_resource_pool_by_id_status_code_is_404_when_not_found(
            self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/resourcePool/{str(uuid.uuid4())}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_resource_pool_by_id_responds_with_single_resource(
            self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}"
        )

        resource = response.json()

        assert isinstance(resource, dict)

        assert resource["name"] == "test_name"

    def test_get_resource_pool_by_id_responds_with_defined_query_fields(
            self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}",
            params={"fields": "name"},
        )

        resource = response.json()

        assert "category" not in resource

    def test_get_resources_pool_responds_with_mandatory_fields_always(
            self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}",
            params={"fields": "name"},
        )

        resource = response.json()

        assert "href" in resource
        assert "name" in resource


class TestUpdateResourceByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "get", mocks.get)

    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_delete(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "update", mocks.update)

    @pytest.fixture(scope="function", autouse=True)
    def test_update_resource_pool_by_id_status_code_is_200(
            self, client: TestClient
    ) -> None:
        response = client.patch(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}",
            content=json.dumps({"name": "test_name"}),
        )

        assert response.status_code == status.HTTP_200_OK
        # response.json()["name"] = "test_name1"
        #
        # assert response.json()["name"] == "test_name1"

    # def test_update_resource_pool_by_id_status_code_is_404_when_not_found(
    #     self, client: TestClient
    # ) -> None:
    #     response = client.patch(
    #         f"{settings.API_PREFIX}/resourcePool/{str(uuid.uuid4())}",
    #         content=json.dumps({"name": "test_name"}),
    #     )
    #     assert "id" not in response.json()
    #     assert response.status_code == status.HTTP_404_NOT_FOUND

    # def test_update_resource_pool_by_id_status_code_is_200(
    #     self, client: TestClient
    # ) -> None:
    #     response = client.patch(
    #         f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}",
    #         content=json.dumps({"name": "test_name"}),
    #     )
    #     assert "id" in response.json()
    #     assert response.status_code == status.HTTP_200_OK


class TestDeleteResourcePooleByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "get", mocks.get)

    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_delete(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "delete", mocks.delete)

    def test_delete_resource_pool_by_id_status_code_is_200(self, client: TestClient) -> None:
        response = client.delete(
            f"{settings.API_PREFIX}/resourcePool/{mocks.EXISTING_RESOURCE.id}"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_resource_pool_by_id_status_code_is_404_when_not_found(
            self, client: TestClient
    ) -> None:
        response = client.delete(f"{settings.API_PREFIX}/resourcePool/{str(uuid.uuid4())}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
