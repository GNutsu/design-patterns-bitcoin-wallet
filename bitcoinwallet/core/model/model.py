from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    api_key: str


class CreateWalletResponse(BaseModel):
    wallet_address: str
    balance_btc: float
    balance_usd: float


class CreateTransactionRequest(BaseModel):
    from_wallet_address: str
    to_wallet_address: str
    amount: int


class TransactionModel(BaseModel):
    from_wallet_address: str
    to_wallet_address: str
    amount: int
    fee_price: int


class ListTransactionsResponse(BaseModel):
    transactions: list[TransactionModel]
