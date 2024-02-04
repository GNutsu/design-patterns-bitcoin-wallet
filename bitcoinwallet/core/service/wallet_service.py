import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bitcoinwallet.core.logger import ILogger
from bitcoinwallet.core.model.entity import WalletEntity
from bitcoinwallet.core.model.exception.wallet_exception import (
    NotEnoughBalanceException,
    WalletNotFoundException,
    WalletsLimitExceededException,
)
from bitcoinwallet.core.repository.repository_factory import IRepositoryFactory


class IWalletService(ABC):
    @abstractmethod
    def create_wallet(self, user_api_key: str) -> str:
        pass

    @abstractmethod
    def get_owner_api_key(self, address: str) -> str:
        pass

    @abstractmethod
    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    @abstractmethod
    def deposit(self, wallet_address: str, amount: int) -> None:
        pass


@dataclass
class WalletService(IWalletService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def create_wallet(self, user_api_key: str) -> str:
        self.logger.info("Creating new wallet")
        users_wallets = IRepositoryFactory.get_repository(WalletEntity).get_by_field("owner_api_key", user_api_key)
        if len(users_wallets) >= 3:
            raise WalletsLimitExceededException(user_api_key)
        wallet_entity = WalletEntity(id=str(uuid.uuid4()),
                                     owner_api_key=user_api_key, balance=100000000,
                                     creation_time=datetime.now().timestamp(),
                                     address=str(uuid.uuid4()))
        self.repository_factory.get_repository(wallet_entity.__class__).create(
            wallet_entity
        )
        return wallet_entity.address

    def get_owner_api_key(self, address: str) -> str:
        wallets: List[WalletEntity] = self.repository_factory.get_repository(WalletEntity) \
            .get_by_field("address", address)
        if wallets is None or len(wallets) == 0:
            raise WalletNotFoundException(address)
        return wallets[0].owner_api_key

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        wallets: List[WalletEntity] = self.repository_factory.get_repository(WalletEntity) \
            .get_by_field("address", wallet_address)
        if wallets is None or len(wallets) == 0:
            raise WalletNotFoundException(wallet_address)
        wallet: WalletEntity = wallets[0]
        if wallet.balance < amount:
            raise NotEnoughBalanceException(wallet_address)
        wallet.balance = wallet.balance - amount
        self.repository_factory.get_repository(WalletEntity).update(wallet)

    def deposit(self, wallet_address: str, amount: int) -> None:
        wallets: List[WalletEntity] = self.repository_factory.get_repository(WalletEntity) \
            .get_by_field("address", wallet_address)
        if wallets is None or len(wallets) == 0:
            raise WalletNotFoundException(wallet_address)
        wallet: WalletEntity = wallets[0]
        wallet.balance = wallet.balance + amount
        self.repository_factory.get_repository(WalletEntity).update(wallet)


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass
