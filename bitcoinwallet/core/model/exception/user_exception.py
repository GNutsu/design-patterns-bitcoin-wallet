from bitcoinwallet.core.model.exception.exception import NotFoundException

class UserNotFoundException(NotFoundException):
    def __init__(self, api_key: str) -> None:
        self.msg: str = "User with api_key: " + api_key + " doesn't exist"

    def get_msg(self) -> str:
        return self.msg

