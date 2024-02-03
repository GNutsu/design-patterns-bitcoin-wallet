from abc import ABC, abstractmethod

from bitcoinwallet.core.repository.repository import IRepository, NullRepository


class IRepositoryFactory(ABC):
    @abstractmethod
    def get_repository(self) -> IRepository:
        pass


class NullRepositoryFactory(IRepositoryFactory):
    def get_repository(self) -> IRepository:
        return NullRepository()
