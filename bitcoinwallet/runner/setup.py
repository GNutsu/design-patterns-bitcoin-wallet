from fastapi import FastAPI

from bitcoinwallet.core.model.exception import ForbiddenException, NotFoundException
from bitcoinwallet.core.repository.repository_factory import RepositoryFactory
from bitcoinwallet.core.service.bitcoin_service import BitcoinServiceBuilder
from bitcoinwallet.core.service.user_service import UserServiceBuilder
from bitcoinwallet.infra.fastapi.bitcoin_controller import bitcoin_api
from bitcoinwallet.infra.fastapi.exceptionhandler.error_handler import (
    forbidden_exception_handler,
    not_found_exception_handler,
)


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(bitcoin_api)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)

    repository_factory = RepositoryFactory()
    user_service = (
        UserServiceBuilder().set_repository_factory(repository_factory).build()
    )

    bitcoin_service = BitcoinServiceBuilder().set_user_service(user_service).build()

    app.state.bitcoin = bitcoin_service
    return app
