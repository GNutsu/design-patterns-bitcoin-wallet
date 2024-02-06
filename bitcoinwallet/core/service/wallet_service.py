import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, TypeVar, cast

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from bitcoinwallet.core.model.entity import WalletEntity
from bitcoinwallet.core.model.exception.wallet_exception import (
    InvalidNumericValueException,
    NotEnoughBalanceException,
    UserHasNoRightOnWalletException,
    WalletNotFoundException,
    WalletsLimitExceededException,
)
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from bitcoinwallet.core.util import datetime_now
from definitions import INITIAL_WALLET_BALANCE, MAX_WALLETS_PER_USER

TWalletServiceBuilder = TypeVar("TWalletServiceBuilder", bound="WalletServiceBuilder")


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

    @abstractmethod
    def has_uer_wallet(self, user_api_key: str, address: str) -> bool:
        pass

    @abstractmethod
    def get_wallet_balance(self, api_key: str, wallet_address: str) -> int:
        pass


@dataclass
class WalletService(IWalletService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def _get_wallet_by_address(self, address: str) -> WalletEntity:
        wallets: List[WalletEntity] = cast(
            list[WalletEntity],
            self.repository_factory.get_repository(WalletEntity).get_by_field(
                "address", address
            ),
        )
        if wallets is None or len(wallets) == 0:
            self.logger.error(f"Wallet not found: {address}")
            raise WalletNotFoundException(address)
        return wallets[0]

    def create_wallet(self, user_api_key: str) -> str:
        self.logger.info("Creating new wallet")
        users_wallets = cast(
            list[WalletEntity],
            self.repository_factory.get_repository(WalletEntity).get_by_field(
                "owner_api_key", user_api_key
            ),
        )
        self.logger.info(
            f"User with api_key {user_api_key} has {len(users_wallets)} wallets"
        )

        if len(users_wallets) >= MAX_WALLETS_PER_USER:
            self.logger.error(f"Wallets limit exceeded for user: {user_api_key}")
            raise WalletsLimitExceededException(user_api_key)
        wallet_entity = WalletEntity(
            id=str(uuid.uuid4()),
            owner_api_key=user_api_key,
            balance=INITIAL_WALLET_BALANCE,
            creation_time=datetime_now(),
            address=str(uuid.uuid4()),
        )
        self.repository_factory.get_repository(WalletEntity).create(wallet_entity)
        self.logger.info("Successfully inserted a new wallet")
        return wallet_entity.address

    def get_owner_api_key(self, address: str) -> str:
        wallet = self._get_wallet_by_address(address)
        return wallet.owner_api_key

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        if self.get_owner_api_key(wallet_address) != user_api_key:
            raise UserHasNoRightOnWalletException(user_api_key)
        if amount < 0:
            self.logger.error(f"Invalid amount for withdrawal: {amount}")
            raise InvalidNumericValueException("Amount must be positive")
        wallet = self._get_wallet_by_address(wallet_address)
        if wallet.balance < amount:
            self.logger.error(f"Not enough balance in wallet: {wallet_address}")
            raise NotEnoughBalanceException(wallet_address)
        wallet.balance -= amount
        self.repository_factory.get_repository(WalletEntity).update(wallet)

    def deposit(self, wallet_address: str, amount: int) -> None:
        if amount < 0:
            self.logger.error(f"Invalid amount for deposit: {amount}")
            raise InvalidNumericValueException("Amount must be positive")
        wallet = self._get_wallet_by_address(wallet_address)
        wallet.balance += amount
        self.repository_factory.get_repository(WalletEntity).update(wallet)

    def get_wallet_balance(self, api_key: str, wallet_address: str) -> int:
        wallet = self._get_wallet_by_address(wallet_address)
        if wallet.owner_api_key != api_key:
            raise UserHasNoRightOnWalletException(api_key)
        return wallet.balance

    def has_uer_wallet(self, api_key: str, address: str) -> bool:
        self.logger.info("Checking if user has wallet with address")
        wallets = self.repository_factory.get_repository(WalletEntity).get_by_field(
            "owner_api_key", api_key
        )
        for wallet in wallets:
            addr = cast(WalletEntity, wallet).address
            if addr == address:
                return True
        return False


class NullWalletService(IWalletService):
    def create_wallet(self, api_key: str) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self, address: str) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass

    def get_wallet_balance(self, api_key: str, wallet_address: str) -> int:
        return 0

    def has_uer_wallet(self, user_api_key: str, address: str) -> bool:
        return False


class WalletServiceBuilder:
    def __init__(self) -> None:
        self.service = WalletService(
            logger=ConsoleLogger(WalletService.__name__),
            repository_factory=NullRepositoryFactory(),
        )

    def set_logger(
        self: TWalletServiceBuilder, logger: ILogger
    ) -> TWalletServiceBuilder:
        self.service.logger = logger
        return self

    def set_repository_factory(
        self: TWalletServiceBuilder, repository_factory: IRepositoryFactory
    ) -> TWalletServiceBuilder:
        self.service.repository_factory = repository_factory
        return self

    def build(self) -> WalletService:
        return self.service

    def has_uer_wallet(self, user_api_key: str, address: str) -> bool:
        return False
