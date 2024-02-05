from abc import ABC, abstractmethod
from typing import List

from bitcoinwallet.core.logger import ILogger
from bitcoinwallet.core.model.entity import WalletEntity
from bitcoinwallet.core.model.exception import UserHasNoRightOnWalletException
from bitcoinwallet.core.repository.repository_factory import IRepositoryFactory


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
    def has_uer_wallet(self, user_api_key: str, address: str) -> bool:
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

    def has_uer_wallet(self, api_key: str, address: str) -> bool:
        self.logger.info("Checking if user has wallet with address")
        wallets = self.repository_factory.get_repository(WalletEntity).get_by_field(
            "owner_api_key", api_key
        )
        return any(wallet.id == address for wallet in wallets)


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass

    def has_uer_wallet(self, user_api_key: str, address: str) -> bool:
        pass
