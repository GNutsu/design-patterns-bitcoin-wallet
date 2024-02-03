from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from bitcoinwallet.core.service.user_service import IUserService, NullUserService
from bitcoinwallet.core.service.wallet_service import IWalletService, NullWalletService
from bitcoinwallet.core.utils import ConsoleLogger, ILogger

TBitcoinService = TypeVar("TBitcoinService", bound="BitcoinServiceBuilder")


class IBitcoinService(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass


@dataclass
class BitcoinService(IBitcoinService):
    user_service: IUserService
    wallet_service: IWalletService
    logger: ILogger

    def create_user(self) -> str:
        self.logger.info("Creating user")
        api_key = self.user_service.create_user()
        return api_key


class BitcoinServiceBuilder:
    def __init__(self) -> None:
        self.service = BitcoinService(
            logger=ConsoleLogger(BitcoinService.__name__),
            user_service=NullUserService(),
            wallet_service=NullWalletService(),
        )

    def set_logger(self: TBitcoinService, logger: ILogger) -> TBitcoinService:
        self.service.logger = logger
        return self

    def set_user_service(
        self: TBitcoinService, user_service: IUserService
    ) -> TBitcoinService:
        self.service.user_service = user_service
        return self

    def set_wallet_service(
        self: TBitcoinService, wallet_service: IWalletService
    ) -> TBitcoinService:
        self.service.wallet_service = wallet_service
        return self

    def build(self) -> BitcoinService:
        return self.service
