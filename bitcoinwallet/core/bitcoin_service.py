from abc import ABC, abstractmethod
from dataclasses import dataclass

from bitcoinwallet.core.bitcoin_repository import (
    BitcoinRepositorySqlite,
    IBitcoinRepository,
)
from bitcoinwallet.core.utils import ConsoleLogger, ILogger


class IBitcoinService(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass


@dataclass
class BitcoinService(IBitcoinService):
    repository: IBitcoinRepository

    def __init__(self) -> None:
        self.repository = BitcoinRepositorySqlite()
        self.logger: ILogger = ConsoleLogger(self.__class__.__name__)

    def create_user(self) -> str:
        self.logger.info("Creating new user")
        api_key = self.repository.create_user()
        self.logger.info(f"Created user, api_key = {api_key}")
        return api_key
