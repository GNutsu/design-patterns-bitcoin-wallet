from abc import ABC
from dataclasses import dataclass


class ILogger(ABC):
    def info(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass


@dataclass
class ConsoleLogger(ILogger):
    class_name: str

    def info(self, msg: str) -> None:
        print("INFO: " + self.get_logging_message(msg))

    def error(self, msg: str) -> None:
        print("ERROR: " + self.get_logging_message(msg))

    def get_logging_message(self, msg: str) -> str:
        return f"LOGGING CLASS: {self.class_name}: " + msg
