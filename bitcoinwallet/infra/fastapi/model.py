from datetime import datetime
from typing import List

from pydantic import BaseModel

from bitcoinwallet.core.repository.entity import TransactionEntity


class CreateUserResponse(BaseModel):
    api_key: str


class CreateWalletResponse(BaseModel):
    wallet_address: str
    balance_btc: float
    balance_usd: float


class CreateTransactionRequest(BaseModel):
    user_api_key: str
    from_wallet_address: str
    to_wallet_address: str
    amount: int


class GetTransactionsRequest(BaseModel):
    user_api_key: str


class Transaction:
    from_addr: str
    to_addr: str
    amount: int
    fee_cost: int
    transaction_time: datetime


class GetTransactionsResponse(BaseModel):
    list: List[Transaction]
