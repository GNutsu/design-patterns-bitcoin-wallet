from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


class Entity(ABC):
    @abstractmethod
    def get_table_name(self) -> str:
        pass


class NullEntity(Entity):
    def get_table_name(self) -> str:
        return "NULL TABLE"


@dataclass
class UserEntity(Entity):
    table_name: str = field(default="users", init=False)
    api_key: str
    wallet_count: int

    def get_table_name(self) -> str:
        return self.table_name


@dataclass
class TransactionEntity(Entity):
    table_name: str = field(default="transactions", init=False)
    id: str
    from_addr: str
    to_addr: str
    amount: int
    fee_cost: int
    transaction_time: datetime

    def get_table_name(self) -> str:
        return self.table_name


@dataclass
class WalletEntity(Entity):
    table_name: str = field(default="wallets", init=False)
    address: str
    user_api_key: str
    balance_satoshi: int
    creation_time: datetime

    def get_table_name(self) -> str:
        return self.table_name
