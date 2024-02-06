import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, TypeVar

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from bitcoinwallet.core.model.exception.wallet_exception import (
    UserHasNoRightOnWalletException,
)
from bitcoinwallet.core.model.model import CreateTransactionResponse, TransactionModel
from bitcoinwallet.core.service.currency_api_client import (
    ICurrencyApiClient,
    NullCurrencyApiClient,
)
from bitcoinwallet.core.service.transaction_service import (
    ITransactionService,
    NullTransactionService,
)
from bitcoinwallet.core.service.user_service import IUserService, NullUserService
from bitcoinwallet.core.service.wallet_service import IWalletService, NullWalletService
from bitcoinwallet.core.util import CurrencyExchangeUtil
from definitions import BITCOIN_FEE_PERCENTAGE

TBitcoinService = TypeVar("TBitcoinService", bound="BitcoinServiceBuilder")


class IBitcoinService(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass

    @abstractmethod
    def create_transaction(
        self,
        user_api_key: str,
        from_wallet_addr: str,
        to_wallet_addr: str,
        amount: float,
    ) -> CreateTransactionResponse:
        pass

    @abstractmethod
    def get_addr_transactions(
        self, user_api_key: str, address: str
    ) -> List[TransactionModel]:
        pass

    @abstractmethod
    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        pass

    @abstractmethod
    def admin_valid(self, api_key: str) -> bool:
        pass

    @abstractmethod
    def user_valid(self, api_key: str) -> bool:
        pass

    @abstractmethod
    def get_wallet_balance(
        self, api_key: str, wallet_address: str
    ) -> Tuple[float, float]:
        pass

    @abstractmethod
    def create_wallet(self, api_key: str) -> Tuple[str, float, float]:
        pass

    @abstractmethod
    def get_statistics(self, admin_api_key: str) -> tuple[int, float]:
        pass


@dataclass
class BitcoinService(IBitcoinService):
    user_service: IUserService
    wallet_service: IWalletService
    transaction_service: ITransactionService
    logger: ILogger
    currency_api_client: ICurrencyApiClient

    def create_user(self) -> str:
        self.logger.info("Creating user")
        api_key = self.user_service.create_user()
        return api_key

    def get_addr_transactions(
        self, user_api_key: str, address: str
    ) -> List[TransactionModel]:
        self.logger.info(
            f"Getting transactions for user_api_key:"
            f" {user_api_key} from_wallet_addr: {address}"
        )
        if not self.wallet_service.has_uer_wallet(user_api_key, address):
            raise UserHasNoRightOnWalletException(user_api_key=user_api_key)
        transactions_list = self.transaction_service.get_addr_transactions(
            user_api_key, address
        )
        return transactions_list

    def create_transaction(
        self,
        user_api_key: str,
        from_wallet_addr: str,
        to_wallet_addr: str,
        amount: float,
    ) -> CreateTransactionResponse:
        self.logger.info(
            f"Creating transaction user_api_key: {user_api_key}, "
            f"from_wallet_addr: {from_wallet_addr} "
            f"to_wallet_addr: {to_wallet_addr}, amount: {amount}"
        )
        first_owner = self.wallet_service.get_owner_api_key(address=from_wallet_addr)
        second_owner = self.wallet_service.get_owner_api_key(address=to_wallet_addr)
        fee_for_transaction = 0

        amount_in_satoshi = CurrencyExchangeUtil.bitcoin_to_satoshi(amount)

        if first_owner != second_owner:
            fee_for_transaction = math.ceil(
                amount_in_satoshi * BITCOIN_FEE_PERCENTAGE / 100
            )

        self.logger.info(f"Fee for transaction is:  {fee_for_transaction}")
        self.wallet_service.withdraw(
            user_api_key=user_api_key,
            wallet_address=from_wallet_addr,
            amount=amount_in_satoshi + fee_for_transaction,
        )
        self.wallet_service.deposit(
            wallet_address=to_wallet_addr, amount=amount_in_satoshi
        )
        transaction_model = TransactionModel(
            from_wallet_address=from_wallet_addr,
            to_wallet_address=to_wallet_addr,
            amount=amount,
            fee_price=fee_for_transaction,
        )
        transaction_id = self.transaction_service.create_transaction(
            from_addr=from_wallet_addr,
            to_addr=to_wallet_addr,
            amount=amount_in_satoshi,
            fee_cost=fee_for_transaction,
        )
        return CreateTransactionResponse(
            transaction_id=transaction_id, transaction=transaction_model
        )

    def get_transactions(self, api_key: str) -> list[TransactionModel]:
        self.logger.info(f"Collecting transactions for {api_key}")
        return self.transaction_service.get_transactions(api_key)

    def admin_valid(self, api_key: str) -> bool:
        self.logger.info(f"Checking admin validity: {api_key}")
        return self.user_service.admin_valid(api_key)

    def user_valid(self, api_key: str) -> bool:
        self.logger.info(f"Checking user validity: {api_key}")
        return self.user_service.user_valid(api_key)

    def get_wallet_balance(
        self, api_key: str, wallet_address: str
    ) -> Tuple[float, float]:
        self.logger.info(f"Fetching balance for wallet: {wallet_address}")
        satoshi_balance = self.wallet_service.get_wallet_balance(
            api_key, wallet_address
        )
        btc_balance = CurrencyExchangeUtil.satoshi_to_bitcoin(satoshi_balance)

        usd_balance = CurrencyExchangeUtil.bitcoin_to_usd(
            btc_balance, self.currency_api_client
        )
        return btc_balance, usd_balance

    def create_wallet(self, api_key: str) -> Tuple[str, float, float]:
        self.logger.info(f"Creating wallet for user: {api_key}")
        wallet_address = self.wallet_service.create_wallet(api_key)
        btc_balance, usd_balance = self.get_wallet_balance(api_key, wallet_address)
        return wallet_address, btc_balance, usd_balance

    def get_statistics(self, admin_api_key: str) -> tuple[int, float]:
        return self.transaction_service.get_statistics(admin_api_key)


class BitcoinServiceBuilder:
    def __init__(self) -> None:
        self.service = BitcoinService(
            logger=ConsoleLogger(BitcoinService.__name__),
            user_service=NullUserService(),
            wallet_service=NullWalletService(),
            transaction_service=NullTransactionService(),
            currency_api_client=NullCurrencyApiClient(),
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

    def set_transaction_service(
        self: TBitcoinService, transaction_service: ITransactionService
    ) -> TBitcoinService:
        self.service.transaction_service = transaction_service
        return self

    def set_currency_api_client(
        self: TBitcoinService, currency_api_client: ICurrencyApiClient
    ) -> TBitcoinService:
        self.service.currency_api_client = currency_api_client
        return self

    def build(self) -> BitcoinService:
        return self.service
