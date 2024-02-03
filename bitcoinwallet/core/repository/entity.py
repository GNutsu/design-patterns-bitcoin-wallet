from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Entity(ABC):
    @abstractmethod
    def get_table_name(self) -> str:
        pass


class NullEntity(Entity):
    def get_table_name(self) -> str:
        return "NULL TABLE"


@dataclass
class UserEntity(Entity):
    table_name: str = field(default="users", init=False)
    api_key: str
    wallet_count: int

    def get_table_name(self) -> str:
        return self.table_name
