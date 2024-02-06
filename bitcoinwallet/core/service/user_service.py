import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from bitcoinwallet.core.logger import ConsoleLogger, ILogger
from bitcoinwallet.core.model.entity import UserEntity
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from definitions import ADMIN_API_KEY

TUserService = TypeVar("TUserService", bound="UserServiceBuilder")


class IUserService(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass

    @abstractmethod
    def user_valid(self, api_key: str) -> bool:
        pass

    @abstractmethod
    def admin_valid(self, api_key: str) -> bool:
        pass


@dataclass
class UserService(IUserService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def create_user(self) -> str:
        self.logger.info("Creating new user")
        api_key = str(uuid.uuid4())
        user_entity = UserEntity(api_key=api_key, wallet_count=0)
        self.repository_factory.get_repository(user_entity.__class__).create(
            user_entity
        )
        self.logger.info(f"Created user, api_key = {api_key}")
        return api_key

    def user_valid(self, api_key: str) -> bool:
        self.logger.info("Checking if user is valid")
        return (
            self.repository_factory.get_repository(UserEntity).read(api_key) is not None
        )

    def admin_valid(self, api_key: str) -> bool:
        self.logger.info("Checking if admin is valid")
        return api_key == ADMIN_API_KEY


class UserServiceBuilder:
    def __init__(self) -> None:
        self.service = UserService(
            logger=ConsoleLogger(UserService.__name__),
            repository_factory=NullRepositoryFactory(),
        )

    def set_logger(self: TUserService, logger: ILogger) -> TUserService:
        self.service.logger = logger
        return self

    def set_repository_factory(
        self: TUserService, repository_factory: IRepositoryFactory
    ) -> TUserService:
        self.service.repository_factory = repository_factory
        return self

    def build(self) -> UserService:
        return self.service


class NullUserService(IUserService):
    def create_user(self) -> str:
        return "USER NOT CREATED"

    def user_valid(self, api_key: str) -> bool:
        return False

    def admin_valid(self, api_key: str) -> bool:
        return False
