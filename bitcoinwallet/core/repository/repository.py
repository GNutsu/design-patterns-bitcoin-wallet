from abc import ABC, abstractmethod

from bitcoinwallet.core.repository.entity import Entity, NullEntity


class IRepository(ABC):
    @abstractmethod
    def get(self) -> Entity:
        pass

    @abstractmethod
    def save(self, entity: Entity) -> None:
        pass


class NullRepository(IRepository):
    def get(self) -> Entity:
        return NullEntity()

    def save(self, entity: Entity) -> None:
        pass
