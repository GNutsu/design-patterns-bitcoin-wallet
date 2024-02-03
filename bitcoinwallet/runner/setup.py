from fastapi import FastAPI

from bitcoinwallet.core.repository.repository_factory import NullRepositoryFactory
from bitcoinwallet.core.service.bitcoin_service import BitcoinServiceBuilder
from bitcoinwallet.core.service.user_service import UserServiceBuilder
from bitcoinwallet.infra.fastapi.bitcoin_controller import bitcoin_api


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(bitcoin_api)

    repository_factory = NullRepositoryFactory()
    user_service = (
        UserServiceBuilder().set_repository_factory(repository_factory).build()
    )

    bitcoin_service = BitcoinServiceBuilder().set_user_service(user_service).build()

    app.state.bitcoin = bitcoin_service
    return app
