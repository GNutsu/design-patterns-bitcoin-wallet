import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


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
