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
