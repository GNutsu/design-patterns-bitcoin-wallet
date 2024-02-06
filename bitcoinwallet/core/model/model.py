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
    amount: float


class TransactionModel(BaseModel):
    from_wallet_address: str
    to_wallet_address: str
    amount: float
    fee_price: float


class CreateTransactionResponse(BaseModel):
    transaction_id: str
    transaction: TransactionModel


class ListTransactionsResponse(BaseModel):
    transactions: list[TransactionModel]


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


class StatisticsResponse(BaseModel):
    transactions_num: int
    platform_profit: float
