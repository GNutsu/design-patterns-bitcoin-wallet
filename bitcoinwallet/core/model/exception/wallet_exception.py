from bitcoinwallet.core.model.exception.exception import (
    ForbiddenException,
    NotFoundException,
)


class WalletNotFoundException(NotFoundException):
    def get_msg(self) -> str:
        return f"Wallet with address: {self.wallet_address} not found."

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address


class UserHasNoRightOnWalletException(ForbiddenException):
    def get_msg(self) -> str:
        return (
            f"User with api_key: {self.api_key} "
            f"does not have permission on this wallet."
        )

    def __init__(self, user_api_key: str):
        self.api_key = user_api_key


class WalletsLimitExceededException(ForbiddenException):
    def __init__(self, user_api_key: str):
        self.api_key = user_api_key

    def get_msg(self) -> str:
        return f"User with api_key: {self.api_key} has reached the wallet limit."


class NoRightOnWalletException(ForbiddenException):
    def __init__(self, user_api_key: str, wallet_address: str):
        self.user_api_key = user_api_key
        self.wallet_address = wallet_address

    def get_msg(self) -> str:
        return (
            f"User with api_key: {self.user_api_key} "
            f"does not have rights to access wallet {self.wallet_address}. "
        )


class NotEnoughBalanceException(ForbiddenException):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def get_msg(self) -> str:
        return (
            f"Wallet with address: {self.wallet_address} does not have enough balance."
        )
