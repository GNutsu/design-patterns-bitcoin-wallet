import os
from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app
from definitions import TEST_DB_NAME
from resources.db.sql import db_setup
from tests.test_repository_factory import TestRepositoryFactory


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    db_setup(TEST_DB_NAME)

    yield TestClient(init_app(TestRepositoryFactory.get_instance()))

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_user(client: TestClient) -> None:
    response = client.post("/users")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["api_key"] is not None
