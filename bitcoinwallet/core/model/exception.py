from abc import ABC, abstractmethod


class NotFoundException(Exception, ABC):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class UserNotFoundException(NotFoundException):
    def __init__(self, api_key: str) -> None:
        self.msg: str = "User with api_key: " + api_key + " doesn't exist"

    def get_msg(self) -> str:
        return self.msg


class ForbiddenException(Exception, ABC):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class UserHasNoRightOnWalletException(ForbiddenException):
    def __init__(self, api_key: str, wallet_address: str) -> None:
        self.msg: str = (
            f"User with api_key: {api_key} has no rights on"
            f" wallet address: {wallet_address}"
        )

    def get_msg(self) -> str:
        return self.msg
