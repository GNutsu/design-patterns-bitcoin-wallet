from fastapi import FastAPI

from bitcoinwallet.core.bitcoin_service import BitcoinService
from bitcoinwallet.infra.fastapi.bitcoin_controller import bitcoin_api


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(bitcoin_api)

    app.state.bitcoin = BitcoinService()
    return app
