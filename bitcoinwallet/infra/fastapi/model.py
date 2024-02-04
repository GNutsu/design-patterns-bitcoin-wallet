from pydantic import BaseModel


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


class WalletBalanceResponse(BaseModel):
    btc_balance: float
    usd_balance: float


class TransactionResponse(BaseModel):
    transaction_id: str
    source_wallet_address: str
    destination_wallet_address: str
    amount: float
    fee: float
    timestamp: str
