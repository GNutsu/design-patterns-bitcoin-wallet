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

    TestRepositoryFactory.get_instance().close_connections()

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_create_transaction(client: TestClient) -> None:
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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["transaction_id"] is not None
    assert response.json()["transaction"]["amount"] == amount


def test_transaction_effect(client: TestClient) -> None:
    response = client.post("/users")
    api_key = response.json()["api_key"]

    headers = {
        "X-API-KEY": api_key,
    }

    response = client.post("/wallets", headers=headers)
    from_wallet_address = response.json()["wallet_address"]
    from_wallet_balance = response.json()["balance_btc"]

    response = client.post("/wallets", headers=headers)
    to_wallet_address = response.json()["wallet_address"]
    to_wallet_balance = response.json()["balance_btc"]

    amount = 0.3

    request = {
        "from_wallet_address": from_wallet_address,
        "to_wallet_address": to_wallet_address,
        "amount": amount,
    }

    response = client.post("/transactions", headers=headers, json=request)

    to_response = client.get(f"/wallets/{to_wallet_address}", headers=headers)
    from_response = client.get(f"/wallets/{from_wallet_address}", headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert from_response.json()["btc_balance"] == from_wallet_balance - amount
    assert to_response.json()["btc_balance"] == to_wallet_balance + amount


def test_fee_transaction(client: TestClient) -> None:
    response_one = client.post("/users")
    api_key_one = response_one.json()["api_key"]

    response_two = client.post("/users")
    api_key_two = response_two.json()["api_key"]

    headers_one = {
        "X-API-KEY": api_key_one,
    }

    headers_two = {
        "X-API-KEY": api_key_two,
    }

    response = client.post("/wallets", headers=headers_one)
    from_wallet_address = response.json()["wallet_address"]
    from_wallet_balance = response.json()["balance_btc"]

    response = client.post("/wallets", headers=headers_two)
    to_wallet_address = response.json()["wallet_address"]

    amount = 0.2

    request = {
        "from_wallet_address": from_wallet_address,
        "to_wallet_address": to_wallet_address,
        "amount": amount,
    }

    response = client.post("/transactions", headers=headers_one, json=request)

    from_response = client.get(f"/wallets/{from_wallet_address}", headers=headers_one)

    assert response.status_code == status.HTTP_201_CREATED
    assert from_response.json()["btc_balance"] < from_wallet_balance - amount


def test_invalid_user_transaction(client: TestClient) -> None:
    response = client.post("/transactions", headers={"X-API-KEY": "NO_USER"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_transaction_from_nonexistent_wallet(client: TestClient) -> None:
    user_response = client.post("/users")
    api_key = user_response.json()["api_key"]
    headers = {"X-API-KEY": api_key}

    transaction_request = {
        "from_wallet_address": "non_existent_wallet_address",
        "to_wallet_address": "some_wallet_address",
        "amount": 0.1,
    }
    transaction_response = client.post(
        "/transactions", headers=headers, json=transaction_request
    )
    assert transaction_response.status_code == status.HTTP_404_NOT_FOUND


def test_transaction_from_another_users_wallet(client: TestClient) -> None:
    user1_response = client.post("/users")
    api_key1 = user1_response.json()["api_key"]
    headers1 = {"X-API-KEY": api_key1}

    wallet1_response = client.post("/wallets", headers=headers1)
    wallet1_address = wallet1_response.json()["wallet_address"]

    user2_response = client.post("/users")
    api_key2 = user2_response.json()["api_key"]
    headers2 = {"X-API-KEY": api_key2}

    # Just wallet
    wallet2_response = client.post("/wallets", headers=headers1)
    wallet2_address = wallet2_response.json()["wallet_address"]

    # Attempt to make a transaction from user1's wallet using user2's API key
    transaction_request = {
        "from_wallet_address": wallet1_address,
        "to_wallet_address": wallet2_address,
        "amount": 0.1,
    }
    transaction_response = client.post(
        "/transactions", headers=headers2, json=transaction_request
    )
    print(transaction_response.json())
    assert transaction_response.status_code == status.HTTP_403_FORBIDDEN


def test_get_addr_transactions_success(client: TestClient) -> None:
    response = client.post("/users")
    user_api_key = response.json()["api_key"]
    headers = {"X-API-KEY": user_api_key}

    response = client.post("/wallets", headers=headers)
    wallet_address = response.json()["wallet_address"]

    response = client.get(f"/wallets/{wallet_address}/transactions", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert "transactions" in response.json()


def test_get_addr_transactions_invalid_api_key(client: TestClient) -> None:
    response = client.post("/users")
    invalid_api_key = response.json()["api_key"]

    response = client.post("/users")
    user_api_key = response.json()["api_key"]
    headers = {"X-API-KEY": user_api_key}

    response = client.post("/wallets", headers=headers)
    wallet_address = response.json()["wallet_address"]

    headers = {"X-API-KEY": invalid_api_key}
    response = client.get(f"/wallets/{wallet_address}/transactions", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
