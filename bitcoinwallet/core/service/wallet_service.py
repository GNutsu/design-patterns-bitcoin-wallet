from abc import ABC, abstractmethod
from typing import List

from bitcoinwallet.core.repository.entity import WalletEntity
from bitcoinwallet.core.repository.repository_factory import IRepositoryFactory
from bitcoinwallet.core.service.exception import UserHasNoRightOnWalletException
from bitcoinwallet.core.utils import ILogger
from bitcoinwallet.infra.fastapi.model import Transaction
from bitcoinwallet.core.model.exception import UserHasNoRightOnWalletException


class IWalletService(ABC):
    @abstractmethod
    def create_wallet(self) -> str:
        pass

    @abstractmethod
    def get_owner_api_key(self) -> str:
        pass

    @abstractmethod
    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    @abstractmethod
    def deposit(self, wallet_address: str, amount: int) -> None:
        pass

    @abstractmethod
    def hasUerWallet(self, user_api_key: str, address: str) -> bool:
        pass


class WalletService(IWalletService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def create_wallet(self) -> str:
        return "PASS"

    def get_owner_api_key(self) -> str:
        return "PASS"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        if not self.get_owner_api_key() != user_api_key:
            raise UserHasNoRightOnWalletException(
                api_key=user_api_key, wallet_address=wallet_address
            )
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass

    def hasUerWallet(self, api_key: str, address: str) -> bool:
        self.logger.info("Checking if user has wallet with address")
        return (
            # self.repository_factory.get_repository().get(api_key, address, WalletEntity.table_name)
            # is not None
            False
        )


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass
