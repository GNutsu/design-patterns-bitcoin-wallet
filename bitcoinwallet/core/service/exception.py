from abc import ABC, abstractmethod


class NotFoundException(ABC, Exception):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class UserNotFoundException(NotFoundException):
    def __init__(self, api_key: str) -> None:
        self.msg: str = "User with api_key: " + api_key + " doesn't exist"

    def get_msg(self) -> str:
        return self.msg


class ForbiddenException(ABC, Exception):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class UserHasNoRightOnWalletException(ForbiddenException):
    def __init__(self, api_key: str, wallet_address: str) -> None:
        self.msg: str = (
            "User with api_key: "
            + api_key
            + " has no rights on wallet address: "
            + wallet_address
        )

    def get_msg(self) -> str:
        return self.msg
