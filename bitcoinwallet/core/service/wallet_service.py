from abc import ABC, abstractmethod


class IWalletService(ABC):
    @abstractmethod
    def create_wallet(self) -> str:
        pass


class NullWalletService(IWalletService):
    def create_wallet(self) -> str:
        return "WALLET NOT CREATED"
