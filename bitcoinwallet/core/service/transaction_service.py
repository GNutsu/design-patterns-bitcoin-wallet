import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, TypeVar

from bitcoinwallet.core.repository.entity import TransactionEntity
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from bitcoinwallet.core.service.exception import UserHasNoRightOnWalletException
from bitcoinwallet.core.utils import ConsoleLogger, ILogger
from bitcoinwallet.infra.fastapi.model import Transaction

TTransactionService = TypeVar("TTransactionService", bound="TransactionServiceBuilder")


class ITransactionService(ABC):
    @abstractmethod
    def create_transaction(
        self, from_addr: str, to_addr: str, amount: int, fee_cost: int
    ) -> str:
        pass

    @abstractmethod
    def get_transactions(self, user_api_key: str, address: str) -> List[Transaction]:
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
            transaction_time=datetime.now(),
        )
        self.repository_factory.get_repository().save(transaction_entity)
        self.logger.info(f"Created transaction, id = {id}")
        return id

    def get_transactions(self, api_key: str, address: str) -> List[Transaction]:
        pass


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
