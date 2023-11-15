import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def reset_environ_between_tests() -> Generator[None, None, None]:
    # Save environ before the test
    old_environ = os.environ.copy()
    yield
    # Restore environ after the test
    os.environ.clear()
    os.environ.update(old_environ)
