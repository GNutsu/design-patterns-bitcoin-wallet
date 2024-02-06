from abc import ABC, abstractmethod


class NotFoundException(Exception, ABC):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class ForbiddenException(Exception, ABC):
    @abstractmethod
    def get_msg(self) -> str:
        pass


class InvalidInputException(Exception, ABC):
    @abstractmethod
    def get_msg(self) -> str:
        pass
