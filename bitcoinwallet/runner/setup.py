from fastapi import FastAPI

from bitcoinwallet.core.model.exception.exception import (
    ForbiddenException,
    InvalidInputException,
    NotFoundException,
)
from bitcoinwallet.core.repository.repository_factory import IRepositoryFactory
from bitcoinwallet.core.service.bitcoin_service import BitcoinServiceBuilder
from bitcoinwallet.core.service.currency_api_client import CurrencyApiClient
from bitcoinwallet.core.service.transaction_service import TransactionServiceBuilder
from bitcoinwallet.core.service.user_service import UserServiceBuilder
from bitcoinwallet.core.service.wallet_service import WalletServiceBuilder
from bitcoinwallet.infra.fastapi.bitcoin_controller import bitcoin_api
from bitcoinwallet.infra.fastapi.exceptionhandler.error_handler import (
    forbidden_exception_handler,
    invalid_input_exception_handler,
    not_found_exception_handler,
)
from definitions import GECKO_CURRENCY_BASE_URL


def init_app(repository_factory: IRepositoryFactory) -> FastAPI:
    app = FastAPI()
    app.include_router(bitcoin_api)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    app.add_exception_handler(InvalidInputException, invalid_input_exception_handler)

    user_service = (
        UserServiceBuilder().set_repository_factory(repository_factory).build()
    )

    transaction_service = (
        TransactionServiceBuilder().set_repository_factory(repository_factory).build()
    )

    wallet_service = (
        WalletServiceBuilder().set_repository_factory(repository_factory).build()
    )

    currency_api_client = CurrencyApiClient(GECKO_CURRENCY_BASE_URL)

    bitcoin_service = (
        BitcoinServiceBuilder()
        .set_user_service(user_service)
        .set_transaction_service(transaction_service)
        .set_wallet_service(wallet_service)
        .set_currency_api_client(currency_api_client)
        .build()
    )

    app.state.bitcoin = bitcoin_service
    return app
