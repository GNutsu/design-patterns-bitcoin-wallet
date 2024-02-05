from pathlib import Path

from fastapi import APIRouter, Depends, status

from bitcoinwallet.core.model.model import (
    CreateTransactionRequest,
    CreateUserResponse,
    ListTransactionsResponse, StatisticsResponse,
)
from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable
from bitcoinwallet.infra.fastapi.interceptor.validity_interceptor import verify_api_key

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
        api_key: str = Depends(verify_api_key),
) -> str:
    return bitcoin_service.create_transaction(
        api_key,
        transaction_request.from_wallet_address,
        transaction_request.from_wallet_address,
        transaction_request.amount,
    )


@bitcoin_api.get("/wallets/{address}/transactions", status_code=status.HTTP_200_OK)
def get_addr_transactions(
        bitcoin_service: BitcoinServiceDependable,
        user_api_key: str,
        address: str = Path(),
) -> ListTransactionsResponse:
    return bitcoin_service.get_addr_transactions(user_api_key, address)


@bitcoin_api.get(
    "/transactions",
    status_code=status.HTTP_200_OK,
    response_model=ListTransactionsResponse,
)
def get_transactions(
        bitcoin_service: BitcoinServiceDependable, api_key: str = Depends(verify_api_key)
) -> ListTransactionsResponse:
    transactions = bitcoin_service.get_transactions(api_key)
    return ListTransactionsResponse(transactions=transactions)

"""
@bitcoin_api.get(
    "/statistics",
    status_code=status.HTTP_200_OK,
    response_model=StatisticsResponse,
)
def get_statistics(
        bitcoin_service: BitcoinServiceDependable, admin_api_key: str
) -> StatisticsResponse:
    statistic = bitcoin_service.get_statistics(admin_api_key)
    return statistic
   
    return StatisticsResponse(transactions_num=statistic[0],
                              platform_profit=statistic[1])
"""
