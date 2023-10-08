import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


class TestRootDocsRedirect:
    def test_root_redirects_with_307(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        response = client.get("/", follow_redirects=False)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    def test_root_redirects_to_docs(
        self, client: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        response = client.get("/", follow_redirects=False)

        assert response.headers["location"] == f"{settings.API_PREFIX}/docs"
