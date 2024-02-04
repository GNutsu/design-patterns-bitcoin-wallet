from typing import List

from fastapi import APIRouter, status, Header, HTTPException

from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable
from bitcoinwallet.infra.fastapi.model import (
    CreateTransactionRequest,
    CreateUserResponse,
    CreateWalletResponse,
    WalletBalanceResponse,
    TransactionResponse,
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


@bitcoin_api.post("wallets", status_code=status.HTTP_201_CREATED, response_model=CreateWalletResponse)
def create_wallet(
        bitcoin_service: BitcoinServiceDependable,
        api_key: str = Header(...)
) -> CreateWalletResponse:
    try:
        wallet_address, balance_btc, balance_usd = bitcoin_service.create_wallet(api_key)
        return CreateWalletResponse(wallet_address=wallet_address, bitcoin_balance=balance_btc, usd_balance=balance_usd)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@bitcoin_api.get("/wallets/{address}", response_model=WalletBalanceResponse)
def get_wallet_balance(
        address: str,
        bitcoin_service: BitcoinServiceDependable,
        api_key: str = Header(...)) -> WalletBalanceResponse:
    try:
        btc_balance, usd_balance = bitcoin_service.get_wallet_balance(api_key, address)
        return WalletBalanceResponse(btc_balance=btc_balance, usd_balance=usd_balance)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")