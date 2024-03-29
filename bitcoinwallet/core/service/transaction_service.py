import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, TypeVar, cast

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from bitcoinwallet.core.model.entity import TransactionEntity, WalletEntity
from bitcoinwallet.core.model.model import TransactionModel
from bitcoinwallet.core.model.query import Logical, Operator
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from bitcoinwallet.core.util import CurrencyExchangeUtil, datetime_now

TTransactionService = TypeVar("TTransactionService", bound="TransactionServiceBuilder")


class ITransactionService(ABC):
    @abstractmethod
    def create_transaction(
        self, from_addr: str, to_addr: str, amount: int, fee_cost: int
    ) -> str:
        pass

    @abstractmethod
    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        pass

    @abstractmethod
    def get_addr_transactions(
        self, user_api_key: str, address: str
    ) -> list[TransactionModel]:
        pass

    @abstractmethod
    def get_statistics(self, admin_api_key: str) -> tuple[int, float]:
        pass


@dataclass
class TransactionService(ITransactionService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def create_transaction(
        self, from_addr: str, to_addr: str, amount: int, fee_cost: int
    ) -> str:
        self.logger.info("Creating new transaction")
        id = str(uuid.uuid4())
        transaction_entity = TransactionEntity(
            id=id,
            from_addr=from_addr,
            to_addr=to_addr,
            amount=amount,
            fee_cost=fee_cost,
            transaction_time=datetime_now(),
        )
        self.repository_factory.get_repository(TransactionEntity).create(
            transaction_entity
        )
        self.logger.info(f"Created transaction, id = {id}")
        return id

    def map_transaction_entity_to_model(
        self, transaction_entity: TransactionEntity
    ) -> TransactionModel:
        return TransactionModel(
            from_wallet_address=transaction_entity.from_addr,
            to_wallet_address=transaction_entity.to_addr,
            amount=CurrencyExchangeUtil.satoshi_to_bitcoin(transaction_entity.amount),
            fee_price=transaction_entity.fee_cost,
        )

    def get_addr_transactions(
        self, api_key: str, address: str
    ) -> list[TransactionModel]:
        transactions = self.repository_factory.get_repository(
            TransactionEntity
        ).query_with_builder(
            [
                ("to_addr", Operator.EQUALS, address),
                Logical.OR,
                ("from_addr", Operator.EQUALS, address),
            ]
        )

        transactions_models = [
            self.map_transaction_entity_to_model(cast(TransactionEntity, transaction))
            for transaction in transactions
        ]
        return transactions_models

    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        self.logger.info(f"Collecting transactions for api_key: {api_key}")
        wallets = self.repository_factory.get_repository(
            WalletEntity
        ).query_with_builder([("owner_api_key", Operator.EQUALS, api_key)])

        transaction_models: List[TransactionModel] = []

        for wallet in wallets:
            wallet_address = cast(WalletEntity, wallet).address
            transactions_for_wallet = self.get_addr_transactions(
                api_key, wallet_address
            )
            transaction_models.extend(transactions_for_wallet)

        return transaction_models

    def get_statistics(self, admin_api_key: str) -> tuple[int, float]:
        all_transactions = self.repository_factory.get_repository(
            TransactionEntity
        ).query_with_builder([])

        transactions_num = len(all_transactions)
        platform_profit_in_satoshi = sum(
            cast(TransactionEntity, transaction).fee_cost
            for transaction in all_transactions
        )
        platform_profit = CurrencyExchangeUtil.satoshi_to_bitcoin(
            platform_profit_in_satoshi
        )
        return transactions_num, platform_profit


class TransactionServiceBuilder:
    def __init__(self) -> None:
        self.service = TransactionService(
            logger=ConsoleLogger(TransactionService.__name__),
            repository_factory=NullRepositoryFactory(),
        )

    def set_logger(self: TTransactionService, logger: ILogger) -> TTransactionService:
        self.service.logger = logger
        return self

    def set_repository_factory(
        self: TTransactionService, repository_factory: IRepositoryFactory
    ) -> TTransactionService:
        self.service.repository_factory = repository_factory
        return self

    def build(self) -> TransactionService:
        return self.service


class NullTransactionService(ITransactionService):
    def create_transaction(
        self, from_addr: str, to_addr: str, amount: int, fee_cost: int
    ) -> str:
        return "TRANSACTION NOT CREATED"

    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        return []

    def get_addr_transactions(
        self, user_api_key: str, address: str
    ) -> list[TransactionModel]:
        return []

    def get_statistics(self, admin_api_key: str) -> tuple[int, float]:
        return 0, 0.0
