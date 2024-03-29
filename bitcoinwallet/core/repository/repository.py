import sqlite3
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

from bitcoinwallet.core.logger import ILogger
from bitcoinwallet.core.model.entity import Entity
from bitcoinwallet.core.model.query import Logical, Operator

T = TypeVar("T", bound=Entity)


class IRepository(ABC):
    @abstractmethod
    def create(self, entity: T) -> None:
        pass

    @abstractmethod
    def read(self, entity_id: str) -> Optional[Entity]:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        pass

    @abstractmethod
    def get_by_field(self, field_name: str, field_value: Any) -> List[Entity]:
        pass

    def query_with_builder(
        self,
        conditions: List[Union[Tuple[str, Operator, Any], Logical]],
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Entity]:
        return []

    @abstractmethod
    def close_connection(self) -> None:
        pass


class Repository(IRepository):
    logger: ILogger

    def __init__(self, entity_class: Type[T], db_path: str):
        self._entity_class = entity_class
        self._db_path = db_path
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._cursor = self._connection.cursor()

    def create(self, entity: T) -> None:
        table_name = self._entity_class.get_table_name()
        columns = ", ".join(entity.__dict__.keys())
        placeholders = ", ".join(["?" for _ in entity.__dict__.values()])
        values = tuple(entity.__dict__.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self._cursor.execute(query, values)
        self._connection.commit()

    def read(self, entity_id: str) -> Optional[Entity]:
        table_name = self._entity_class.get_table_name()
        primary_key = self._entity_class.get_primary_key()

        query = f"SELECT * FROM {table_name} WHERE {primary_key} = ?"
        self._cursor.execute(query, (entity_id,))
        result = self._cursor.fetchone()
        return self._create_entity(result) if result else None

    def update(self, entity: T) -> None:
        table_name = self._entity_class.get_table_name()
        set_clause = ", ".join([f"{key} = ?" for key in entity.__dict__.keys()])
        primary_key = self._entity_class.get_primary_key()
        values = tuple(entity.__dict__.values()) + (entity.__dict__[primary_key],)
        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = ?"
        self._cursor.execute(query, values)
        self._connection.commit()

    def delete(self, entity_id: str) -> None:
        table_name = self._entity_class.get_table_name()
        primary_key = self._entity_class.get_primary_key()
        query = f"DELETE FROM {table_name} WHERE {primary_key} = ?"
        self._cursor.execute(query, (entity_id,))
        self._connection.commit()

    def get_by_field(self, field_name: str, field_value: Any) -> List[Entity]:
        table_name = self._entity_class.get_table_name()
        query = f"SELECT * FROM {table_name} WHERE {field_name} = ?"
        self._cursor.execute(query, (field_value,))
        results = self._cursor.fetchall()
        return [self._create_entity(result) for result in results]

    def _build_query(
        self,
        conditions: List[Union[Tuple[str, Operator, Any], Logical]],
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> tuple[str, List[Any]]:
        table_name = self._entity_class.get_table_name()

        query_parts = []
        values = []

        for condition in conditions:
            if isinstance(condition, Logical):
                query_parts.append(condition.value)
            else:
                field, operator, value = condition
                if operator == Operator.IN:
                    query_parts.append(
                        f"{field} {operator.value} ({', '.join(['?' for _ in value])})"
                    )
                    values.extend(value)
                else:
                    query_parts.append(f"{field} {operator.value} ?")
                    values.append(value)

        query = f"SELECT * FROM {table_name}"
        if query_parts:
            query += f" WHERE {' '.join(query_parts)}"

        if order_by:
            query += f" ORDER BY {order_by}"

        if limit:
            query += f" LIMIT {limit}"

        return query, values

    def query_with_builder(
        self,
        conditions: List[Union[Tuple[str, Operator, Any], Logical]],
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Entity]:
        query, values = self._build_query(conditions, order_by, limit)
        self._cursor.execute(query, values)
        results = self._cursor.fetchall()
        return [self._create_entity(result) for result in results]

    def _create_entity(self, result: Any) -> Entity:
        field_names = self._entity_class.__dataclass_fields__.keys()
        entity_data = dict(zip(field_names, result))
        return self._entity_class(**entity_data)

    def close_connection(self) -> None:
        self._connection.close()


class NullRepository(IRepository):
    def create(self, entity: T) -> None:
        pass

    def read(self, entity_id: str) -> Optional[Entity]:
        return None

    def update(self, entity: T) -> None:
        pass

    def delete(self, entity_id: str) -> None:
        pass

    def get_by_field(self, field_name: str, field_value: Any) -> List[Entity]:
        return List[Entity]()

    def close_connection(self) -> None:
        return None
