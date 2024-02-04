from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


class Entity(ABC):
    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        pass


class NullEntity(Entity):
    @staticmethod
    def get_table_name() -> str:
        return "NULL TABLE"


@dataclass
class UserEntity(Entity):
    table_name: str = field(default="users", init=False)
    api_key: str
    wallet_count: int

    @staticmethod
    def get_table_name() -> str:
        return "users"


@dataclass
class TransactionEntity(Entity):
    table_name: str = field(default="transactions", init=False)
    id: str
    from_addr: str
    to_addr: str
    amount: int
    fee_cost: int
    transaction_time: datetime

    @staticmethod
    def get_table_name() -> str:
        return "transactions"


@dataclass
class WalletEntity(Entity):
    table_name: str = field(default="wallets", init=False)
    id: str
    owner_api_key: str
    balance: int
    creation_time: datetime

    @staticmethod
    def get_table_name() -> str:
        return "wallets"
