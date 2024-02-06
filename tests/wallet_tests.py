import pytest
from fastapi import status
from fastapi.testclient import TestClient

from bitcoinwallet.runner.setup import init_app
from definitions import MAX_WALLETS_PER_USER


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


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
