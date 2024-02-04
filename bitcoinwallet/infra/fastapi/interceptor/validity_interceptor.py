from fastapi import Header

from bitcoinwallet.core.model.exception import UserNotFoundException
from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable


def verify_api_key(
    bitcoin_service: BitcoinServiceDependable,
    api_key: str = Header(..., alias="X-API-KEY"),
) -> str:
    if not bitcoin_service.user_valid(api_key):
        raise UserNotFoundException(api_key=api_key)
    return api_key
