from fastapi import APIRouter, Depends, status

from bitcoinwallet.core.model.model import (
    CreateTransactionRequest,
    CreateUserResponse,
    CreateWalletResponse,
    ListTransactionsResponse,
    WalletBalanceResponse,
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
        transaction_request.to_wallet_address,
        transaction_request.amount,
    )


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


@bitcoin_api.post(
    "/wallets", status_code=status.HTTP_201_CREATED, response_model=CreateWalletResponse
)
def create_wallet(
    bitcoin_service: BitcoinServiceDependable, api_key: str = Depends(verify_api_key)
) -> CreateWalletResponse:
    wallet_address, balance_btc, balance_usd = bitcoin_service.create_wallet(api_key)
    return CreateWalletResponse(
        wallet_address=wallet_address,
        balance_btc=balance_btc,
        balance_usd=balance_usd,
    )


@bitcoin_api.get("/wallets/{address}", response_model=WalletBalanceResponse)
def get_wallet_balance(
    address: str,
    bitcoin_service: BitcoinServiceDependable,
    api_key: str = Depends(verify_api_key),
) -> WalletBalanceResponse:
    btc_balance, usd_balance = bitcoin_service.get_wallet_balance(api_key, address)
    return WalletBalanceResponse(btc_balance=btc_balance, usd_balance=usd_balance)
