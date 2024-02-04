import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from bitcoinwallet.core.model.entity import TransactionEntity
from bitcoinwallet.core.model.model import TransactionModel
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from bitcoinwallet.core.util import datetime_now

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

    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        self.logger.info(f"Collecting transactions for api_key: {api_key}")
        return []


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
