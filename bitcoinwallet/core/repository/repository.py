from abc import ABC, abstractmethod

from bitcoinwallet.core.model.entity import Entity, NullEntity


class IRepository(ABC):
    @abstractmethod
    def get(self, id: str, table_name: str) -> Entity:
        pass

    @abstractmethod
    def save(self, entity: Entity) -> None:
        pass


class NullRepository(IRepository):
    def get(self, id: str, table_name: str) -> Entity:
        return NullEntity()

    def save(self, entity: Entity) -> None:
        pass
