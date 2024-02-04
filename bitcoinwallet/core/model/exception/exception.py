from abc import ABC, abstractmethod

class NotFoundException(ABC, Exception):
    @abstractmethod
    def get_msg(self) -> str:
        pass

class ForbiddenException(ABC, Exception):
    @abstractmethod
    def get_msg(self) -> str:
        pass