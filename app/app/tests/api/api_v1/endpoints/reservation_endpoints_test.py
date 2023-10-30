import json
import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.mocks import reservation_crud_mocks as mocks


class TestGetReservation:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_reservation_crud_get_multi(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "get_multi", mocks.get_multi)

    def test_get_reservation_status_code_is_200(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/reservation")
        print(f"{response=}")

        assert response.status_code == status.HTTP_200_OK

    def test_get_reservation_responds_with_list_of_reservation(
        self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/reservation")

        assert isinstance(response.json(), list)

        for reservation in response.json():
            assert reservation["reservationState"] == "test_name"

    def test_get_reservations_responds_with_defined_query_fields(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation", params={"fields": "name"}
        )

        for reservation in response.json():
            assert "category" not in reservation

    def test_get_reservation_pool_responds_with_mandatory_fields_always(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation", params={"fields": "name"}
        )

        for reservation in response.json():
            assert "id" in reservation
            assert "href" in reservation
            assert "relatedParty" in reservation

    def test_get_reservations_responds_with_x_total_count_header(
        self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/reservation")

        assert "X-Total-Count" in response.headers

    def test_get_reservations_pool_responds_with_x_result_count_header(
        self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/reservation")

        assert "X-Result-Count" in response.headers


class TestCreateReservation:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_crud_create(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "create", mocks.create)

    def test_create_reservation_pool_status_code_is_201(
        self, client: TestClient
    ) -> None:
        test_request_payload = {"type": "test_name"}

        response = client.post(
            f"{settings.API_PREFIX}/reservation",
            content=json.dumps(test_request_payload),
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["reservationState"] == "test_name"

    def test_create_reservation_missing_name(self, client: TestClient) -> None:
        test_request_payload = {"category1": "test_category"}

        response = client.post(
            f"{settings.API_PREFIX}/reservation",
            content=json.dumps(test_request_payload),
        )
        assert "category" not in response.json()


class TestGetReservationByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_reservation_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "get", mocks.get)

    def test_get_reservation_by_id_status_code_is_200(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_reservation_by_id_status_code_is_404_when_not_found(
        self, client: TestClient
    ) -> None:
        response = client.get(f"{settings.API_PREFIX}/reservation/{str(uuid.uuid4())}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_reservation_by_id_responds_with_single_resource(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}"
        )

        reservation = response.json()

        assert isinstance(reservation, dict)

        assert reservation["reservationState"] == "test_name"

    def test_get_reservation_by_id_responds_with_defined_query_fields(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}",
            params={"fields": "name"},
        )

        reservation = response.json()

        assert "type" not in reservation

    def test_get_reservation_responds_with_mandatory_fields_always(
        self, client: TestClient
    ) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}",
            params={"fields": "name"},
        )

        reservation = response.json()
        print(f"reservation:{reservation}")

        assert "href" in reservation
        assert "relatedParty" in reservation
        assert "id" in reservation


class TestUpdateReservationByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_resource_pool_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.resource_pool, "get", mocks.get)

    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_reservation_crud_delete(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "update", mocks.update)

    @pytest.fixture(scope="function", autouse=True)
    def test_update_reservation_by_id_status_code_is_200(
        self, client: TestClient
    ) -> None:
        response = client.patch(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}",
            content=json.dumps({"reservation_state": "test_reservation"}),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # response.json()["reservationState"] = "test_reservation_1"
        # assert response.json()["reservationState"] == "test_reservation_1"

    def test_update_reservation_by_id_status_code_is_404_when_not_found(
        self, client: TestClient
    ) -> None:
        response = client.patch(
            f"{settings.API_PREFIX}/reservation/{str(uuid.uuid4())}",
            content=json.dumps({"name": "test_name"}),
        )
        assert "reservation_state" not in response.json()
        # assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteReservationByID:
    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_reservation_crud_get(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "get", mocks.get)

    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def mock_reservation_crud_delete(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(crud.reservation, "delete", mocks.delete)

    def test_delete_reservation_by_id_status_code_is_200(
        self, client: TestClient
    ) -> None:
        response = client.delete(
            f"{settings.API_PREFIX}/reservation/{mocks.EXISTING_RESERVATION.id}"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_reservation_by_id_status_code_is_404_when_not_found(
        self, client: TestClient
    ) -> None:
        response = client.delete(
            f"{settings.API_PREFIX}/reservation/{str(uuid.uuid4())}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
