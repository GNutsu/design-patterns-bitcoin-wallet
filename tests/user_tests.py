import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def test_create_user(client: TestClient) -> None:
    response = client.post("/users")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["api_key"] is not None
