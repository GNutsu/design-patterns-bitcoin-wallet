from abc import ABC, abstractmethod
from dataclasses import dataclass

from bitcoinwallet.core.model.exception.wallet_exception import WalletsLimitExceededException, WalletNotFoundException, \
    NotEnoughBalanceException
from bitcoinwallet.core.repository.entity import WalletEntity
from bitcoinwallet.core.repository.repository_factory import IRepositoryFactory
from bitcoinwallet.core.utils import ILogger


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
        users_wallets = self.repository_factory.get_repository().get_wallets_by_user_api_key(user_api_key)
        if users_wallets >= 3:
            raise WalletsLimitExceededException(user_api_key)

        new_wallet = self.repository_factory.get_repository().create_wallet(user_api_key)
        self.deposit(new_wallet.address, 100000000)
        return new_wallet.address

    def get_owner_api_key(self, address:str) -> str:
        wallet = self.repository_factory.get_repository().get_wallet_by_address(address)
        if wallet is None:
            raise WalletNotFoundException(address)
        return wallet.owner_api_key

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        wallet: WalletEntity = self.repository_factory.get_repository().get_wallet_by_address(wallet_address)
        if wallet.user_api_key != user_api_key:
            raise UserHasNoRightOnWalletException(
                api_key=user_api_key, wallet_address=wallet_address
            )
        if wallet.balance_satoshi < amount:
            raise NotEnoughBalanceException(api_key=user_api_key)
        wallet.set_balance(wallet.get_balance()-amount)
        self.repository_factory.get_wallet_dao().save(wallet)

    def deposit(self, wallet_address: str, amount: int) -> None:
        wallet: WalletEntity = self.repository_factory.get_repository().get_wallet_by_address(wallet_address)
        wallet.set_balance(wallet.get_balance()+amount)
        self.repository_factory.get_wallet_dao().save(wallet)


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass
