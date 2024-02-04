from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


class Entity(ABC):
    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_primary_key() -> str:
        pass


class NullEntity(Entity):
    @staticmethod
    def get_table_name() -> str:
        return "NULL TABLE"

    @staticmethod
    def get_primary_key() -> str:
        return "NULL"


@dataclass
class UserEntity(Entity):
    api_key: str
    wallet_count: int

    @staticmethod
    def get_table_name() -> str:
        return "users"

    @staticmethod
    def get_primary_key() -> str:
        return "api_key"


@dataclass
class WalletEntity(Entity):
    id: str
    owner_api_key: str
    balance: int
    creation_time: datetime

    @staticmethod
    def get_table_name() -> str:
        return "wallets"

    @staticmethod
    def get_primary_key() -> str:
        return "id"


@dataclass
class TransactionEntity(Entity):
    id: str
    from_addr: str
    to_addr: str
    amount: int
    fee_cost: int
    transaction_time: datetime

    @staticmethod
    def get_table_name() -> str:
        return "transactions"

    @staticmethod
    def get_primary_key() -> str:
        return "id"
