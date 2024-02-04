from pathlib import Path

from fastapi import APIRouter, status

from bitcoinwallet.core.service import bitcoin_service
from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable
from bitcoinwallet.infra.fastapi.model import (
    CreateTransactionRequest,
    CreateUserResponse,
    GetTransactionsRequest,
    GetTransactionsResponse,
)

bitcoin_api = APIRouter(tags=["Bitcoin"])


@bitcoin_api.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
def create_user(bitcoin_service: BitcoinServiceDependable) -> CreateUserResponse:
    api_key = bitcoin_service.create_user()
    return CreateUserResponse(api_key=api_key)


@bitcoin_api.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_request: CreateTransactionRequest,
    bitcoin_service: BitcoinServiceDependable,
) -> str:
    return bitcoin_service.create_transaction(
        transaction_request.user_api_key,
        transaction_request.from_wallet_address,
        transaction_request.from_wallet_address,
        transaction_request.amount,
    )


@bitcoin_api.get("/wallets/{address}/transactions", status_code=status.HTTP_200_OK)
def get_transactions(
    bitcoin_service: BitcoinServiceDependable,
    get_transactions_request: GetTransactionsRequest,
    address: str = Path(...),
) -> GetTransactionsResponse:
    return bitcoin_service.get_transactions(
        get_transactions_request.user_api_key, address
    )
