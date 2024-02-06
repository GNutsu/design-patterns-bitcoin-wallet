import os
from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app
from definitions import MAX_WALLETS_PER_USER, TEST_DB_NAME
from resources.db.sql import db_setup
from tests.test_repository_factory import TestRepositoryFactory


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    db_setup(TEST_DB_NAME)

    yield TestClient(init_app(TestRepositoryFactory.get_instance()))

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_wallet(client: TestClient) -> None:
    response = client.post("/users")
    api_key = response.json()["api_key"]

    headers = {
        "X-API-KEY": api_key,
    }

    response = client.post("/wallets", headers=headers)
    address = response.json()["wallet_address"]
    btc_balance = response.json()["balance_btc"]

    assert response.status_code == status.HTTP_201_CREATED
    assert address is not None
    assert btc_balance == 1


def test_invalid_user_create_wallet(client: TestClient) -> None:
    response = client.post("/wallets", headers={"X-API-KEY": "NO_USER"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_wallet_number_limit_exceeded(client: TestClient) -> None:
    response = client.post("/users")
    api_key = response.json()["api_key"]

    headers = {
        "X-API-KEY": api_key,
    }

    for i in range(MAX_WALLETS_PER_USER):
        response = client.post("/wallets", headers=headers)
        address = response.json()["wallet_address"]
        btc_balance = response.json()["balance_btc"]

        assert response.status_code == status.HTTP_201_CREATED
        assert address is not None
        assert btc_balance == 1

    for i in range(2):
        response = client.post("/wallets", headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
