from bitcoinwallet.core.model.exception.exception import (
    ForbiddenException,
    NotFoundException,
)


class WalletNotFoundException(NotFoundException):
    def __init__(self, wallet_address: str):
        super().__init__(f"Wallet with address: {wallet_address} not found.")


class UserHasNoRightOnWalletException(ForbiddenException):
    def __init__(self, user_api_key: str):
        super().__init__(
            f"User with api_key: {user_api_key} "
            f"does not have permission on this wallet."
        )


class WalletsLimitExceededException(ForbiddenException):
    def __init__(self, user_api_key: str):
        super().__init__(
            f"User with api_key: {user_api_key} has reached the wallet limit."
        )


class NoRightOnWalletException(ForbiddenException):
    def __init__(self, user_api_key: str, wallet_address: str):
        super().__init__(
            f"User with api_key: {user_api_key} "
            f"does not have rights to access wallet {wallet_address}."
        )


class NotEnoughBalanceException(ForbiddenException):
    def __init__(self, wallet_address: str):
        super().__init__(
            f"Wallet with address: {wallet_address} does not have enough balance."
        )
