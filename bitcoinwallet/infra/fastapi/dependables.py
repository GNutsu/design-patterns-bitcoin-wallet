from typing import Annotated, Any

from fastapi import Depends
from fastapi.requests import Request

from bitcoinwallet.core.service.bitcoin_service import IBitcoinService


def get_bitcoin_service(request: Request) -> Any:
    return request.app.state.bitcoin


BitcoinServiceDependable = Annotated[IBitcoinService, Depends(get_bitcoin_service)]
