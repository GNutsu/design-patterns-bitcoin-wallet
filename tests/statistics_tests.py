import os
import uuid
from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app
from definitions import ADMIN_API_KEY, TEST_DB_NAME
from resources.db.sql import db_setup
from tests.test_repository_factory import TestRepositoryFactory


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    db_setup(TEST_DB_NAME)

    yield TestClient(init_app(TestRepositoryFactory.get_instance()))

    TestRepositoryFactory.get_instance().close_connections()

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_statistics_inner_transaction(client: TestClient) -> None:
    admin_header = {"X-ADMIN-API-KEY": ADMIN_API_KEY}

    response = client.get("/statistics", headers=admin_header)

    assert response.status_code == status.HTTP_200_OK
    transactions_num1 = response.json()["transactions_num"]
    profits1 = response.json()["platform_profit"]

    response = client.post("/users")
    api_key = response.json()["api_key"]

    headers = {
        "X-API-KEY": api_key,
    }

    response = client.post("/wallets", headers=headers)
    from_wallet_address = response.json()["wallet_address"]

    response = client.post("/wallets", headers=headers)
    to_wallet_address = response.json()["wallet_address"]

    amount = 0.2

    request = {
        "from_wallet_address": from_wallet_address,
        "to_wallet_address": to_wallet_address,
        "amount": amount,
    }

    response = client.post("/transactions", headers=headers, json=request)

    admin_header = {"X-ADMIN-API-KEY": ADMIN_API_KEY}

    response = client.get("/statistics", headers=admin_header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["transactions_num"] == transactions_num1 + 1
    assert response.json()["platform_profit"] == profits1


def test_statistics_with_profit(client: TestClient) -> None:
    admin_header = {"X-ADMIN-API-KEY": ADMIN_API_KEY}

    response = client.get("/statistics", headers=admin_header)

    assert response.status_code == status.HTTP_200_OK
    transactions_num1 = response.json()["transactions_num"]
    profits1 = response.json()["platform_profit"]

    response = client.post("/users")
    api_key = response.json()["api_key"]

    headers = {
        "X-API-KEY": api_key,
    }

    response = client.post("/wallets", headers=headers)
    from_wallet_address = response.json()["wallet_address"]

    response = client.post("/users")
    api_key2 = response.json()["api_key"]

    headers_2 = {"X-API-KEY": api_key2}

    response = client.post("/wallets", headers=headers_2)
    to_wallet_address = response.json()["wallet_address"]

    amount = 0.2

    request = {
        "from_wallet_address": from_wallet_address,
        "to_wallet_address": to_wallet_address,
        "amount": amount,
    }

    response = client.post("/transactions", headers=headers, json=request)

    admin_header = {"X-ADMIN-API-KEY": ADMIN_API_KEY}

    response = client.get("/statistics", headers=admin_header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["transactions_num"] == transactions_num1 + 1
    assert response.json()["platform_profit"] > profits1


def test_statistics_invalid_admin(client: TestClient) -> None:
    invalid_admin = str(uuid.uuid4())
    admin_header = {"X-ADMIN-API-KEY": invalid_admin}

    response = client.get("/statistics", headers=admin_header)

    assert response.status_code == status.HTTP_403_FORBIDDEN
