import os
import sqlite3
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from bitcoinwallet.core.utils import ConsoleLogger, ILogger


class IBitcoinRepository(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass


@dataclass
class BitcoinRepositorySqlite(IBitcoinRepository):
    def __init__(self) -> None:
        self.logger: ILogger = ConsoleLogger(self.__class__.__name__)
        self.database_path = self.get_databaase_file_path()
        self.con = sqlite3.connect(self.database_path, check_same_thread=False)
        self.cur = self.con.cursor()

    def get_databaase_file_path(self) -> str:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        resources_path = os.path.join(current_directory, "..", "..", "resources", "db")
        db_file_path = os.path.join(resources_path, "bw_db.db")
        self.logger.info("DB file path: " + db_file_path)
        return db_file_path

    def create_user(self) -> str:
        self.logger.info("Creating user in database")
        api_key = str(uuid.uuid4())
        self.cur.execute(
            """INSERT INTO users(api_key, wallet_count) VALUES(?, ?)""",
            (api_key, 0),
        )
        self.con.commit()
        return str(uuid.uuid4())
