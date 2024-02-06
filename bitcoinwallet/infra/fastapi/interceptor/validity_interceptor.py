from fastapi import Header

from bitcoinwallet.core.model.exception.user_exception import (
    AdminNotFoundException,
    UserNotFoundException,
)
from bitcoinwallet.infra.fastapi.dependables import BitcoinServiceDependable


def verify_api_key(
    bitcoin_service: BitcoinServiceDependable,
    api_key: str = Header(..., alias="X-API-KEY"),
) -> str:
    if not bitcoin_service.user_valid(api_key):
        raise UserNotFoundException(api_key=api_key)
    return api_key


def verify_admin_api_key(
    bitcoin_service: BitcoinServiceDependable,
    admin_api_key: str = Header(..., alias="X-ADMIN-API-KEY"),
) -> str:
    if not bitcoin_service.admin_valid(admin_api_key):
        raise AdminNotFoundException(api_key=admin_api_key)
    return admin_api_key
