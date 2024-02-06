from abc import ABC, abstractmethod
from typing import Dict, Type

from bitcoinwallet.core.model.entity import Entity
from bitcoinwallet.core.repository.repository import (
    IRepository,
    NullRepository,
    Repository,
)
from definitions import DB_NAME


class IRepositoryFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_db_path() -> str:
        pass

    @classmethod
    @abstractmethod
    def get_instance(cls) -> "IRepositoryFactory":
        pass

    @abstractmethod
    def get_repository(self, entity_class: Type[Entity]) -> IRepository:
        pass


class RepositoryFactory(IRepositoryFactory):
    _instance = None

    def __init__(self) -> None:
        self._dao_map: Dict[Type[Entity], IRepository] = {}

    @staticmethod
    def get_db_path() -> str:
        return DB_NAME

    @classmethod
    def get_instance(cls) -> "IRepositoryFactory":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_repository(self, entity_class: Type[Entity]) -> IRepository:
        if entity_class not in self._dao_map:
            self._initialize_repository(entity_class)
        return self._dao_map[entity_class]

    def _initialize_repository(self, entity_class: Type[Entity]) -> None:
        self._dao_map[entity_class] = Repository(entity_class, self.get_db_path())

    def close_connections(self) -> None:
        for v in self._dao_map.values():
            v.close_connection()


class NullRepositoryFactory(IRepositoryFactory):
    @staticmethod
    def get_db_path() -> str:
        return ""

    @classmethod
    def get_instance(cls) -> "IRepositoryFactory":
        return NullRepositoryFactory()

    def get_repository(self, entity_class: Type[Entity]) -> IRepository:
        return NullRepository()
