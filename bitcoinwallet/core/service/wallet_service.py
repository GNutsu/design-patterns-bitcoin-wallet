from abc import ABC, abstractmethod

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


class WalletService(IWalletService):
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


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"

    def get_owner_api_key(self) -> str:
        return "NO OWNER"

    def withdraw(self, user_api_key: str, wallet_address: str, amount: int) -> None:
        pass

    def deposit(self, wallet_address: str, amount: int) -> None:
        pass
