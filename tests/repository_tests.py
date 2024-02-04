import os
from datetime import datetime
from typing import List, Optional

import pytest

from bitcoinwallet.core.model.entity import TransactionEntity, UserEntity, WalletEntity
from bitcoinwallet.core.repository.repository import IRepository
from bitcoinwallet.core.repository.repository_factory import RepositoryFactory
from definitions import TEST_DB_NAME
from resources.db.sql import db_setup


class TestRepositoryFactory(RepositoryFactory):
    @staticmethod
    def get_db_path() -> str:
        return TEST_DB_NAME


@pytest.fixture(scope="session")
def test_db_setup() -> str:
    db_setup(TEST_DB_NAME)

    yield TEST_DB_NAME

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


date_format: str = "%Y-%m-%d %H:%M:%S.%f"


def test_user_repository(test_db_setup: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )

    api_key: str = "123123"
    wallet_count: int = 0

    user_repo.create(UserEntity(api_key, wallet_count))
    user: Optional[UserEntity] = user_repo.read(api_key)
    assert user and user.api_key == "123123" and user.wallet_count == wallet_count

    wallet_count += 1
    user.wallet_count = wallet_count
    user_repo.update(user)

    updated_user: Optional[UserEntity] = user_repo.read(api_key)
    assert (
        updated_user
        and updated_user.api_key == api_key
        and updated_user.wallet_count == wallet_count
    )

    another_api_key: str = "1234"
    user_repo.create(UserEntity(another_api_key, wallet_count))
    another_user: Optional[UserEntity] = user_repo.read(another_api_key)
    assert (
        another_user
        and another_user.api_key == another_api_key
        and another_user.wallet_count == wallet_count
    )

    users: List[UserEntity] = user_repo.get_by_field("wallet_count", wallet_count)
    assert len(users) == 2

    user_repo.delete(api_key)
    users1: List[UserEntity] = user_repo.get_by_field("wallet_count", wallet_count)
    assert len(users1) == 1


def test_wallet_repository(test_db_setup: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )
    wallet_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        WalletEntity
    )

    api_key: str = "123"
    wallet_count: int = 0

    user_repo.create(UserEntity(api_key, wallet_count))
    _: Optional[UserEntity] = user_repo.read(api_key)

    wallet_addr: str = "12345"
    balance: int = 100000
    creation_time: datetime = datetime.now()
    wallet_repo.create(WalletEntity(wallet_addr, api_key, balance, creation_time))
    wallet: Optional[WalletEntity] = wallet_repo.read(wallet_addr)
    assert (
        wallet
        and wallet.id == wallet_addr
        and wallet.creation_time == creation_time.strftime(date_format)
        and wallet.owner_api_key == api_key
        and wallet.balance == balance
    )

    balance += 100000
    wallet.balance = balance
    wallet_repo.update(wallet)

    updated_wallet: Optional[WalletEntity] = wallet_repo.read(wallet_addr)
    assert updated_wallet and updated_wallet.balance == balance

    another_wallet_addr: str = "123456"
    wallet_repo.create(
        WalletEntity(another_wallet_addr, api_key, balance, datetime.now())
    )

    wallets: List[WalletEntity] = wallet_repo.get_by_field("owner_api_key", api_key)
    assert len(wallets) == 2

    wallet_repo.delete(another_wallet_addr)

    wallets1: List[WalletEntity] = wallet_repo.get_by_field("owner_api_key", api_key)
    assert len(wallets1) == 1


def test_transaction_repository(test_db_setup: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )
    wallet_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        WalletEntity
    )
    transaction_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        TransactionEntity
    )

    user: UserEntity = UserEntity("7856", 1)
    user_repo.create(user)
    wallet1: WalletEntity = WalletEntity("6756", user.api_key, 1000000, datetime.now())
    wallet2: WalletEntity = WalletEntity("6757", user.api_key, 1000000, datetime.now())
    wallet_repo.create(wallet1)
    wallet_repo.create(wallet2)

    tr1_id: str = "2346756"
    amount1: int = 10000
    fee1: int = 10
    time1: datetime = datetime.now()
    transaction_repo.create(
        TransactionEntity(tr1_id, wallet1.id, wallet2.id, amount1, fee1, time1)
    )
    tr1: Optional[TransactionEntity] = transaction_repo.read(tr1_id)
    assert (
        tr1
        and tr1.id == tr1_id
        and tr1.from_addr == wallet1.id
        and tr1.to_addr == wallet2.id
        and tr1.amount == amount1
        and tr1.fee_cost == fee1
        and tr1.transaction_time == time1.strftime(date_format)
    )

    amount1 += 10000
    tr1.amount = amount1
    transaction_repo.update(tr1)
    tr1_updated: Optional[TransactionEntity] = transaction_repo.read(tr1_id)
    assert tr1_updated and tr1_updated.amount == amount1

    tr2_id = "856554554"
    transaction_repo.create(
        TransactionEntity(tr2_id, wallet1.id, wallet2.id, amount1, fee1, datetime.now())
    )

    transactions: List[TransactionEntity] = transaction_repo.get_by_field(
        "from_addr", wallet1.id
    )
    assert len(transactions) == 2

    transaction_repo.delete(tr2_id)
    transactions1: List[TransactionEntity] = transaction_repo.get_by_field(
        "from_addr", wallet1.id
    )
    assert len(transactions1) == 1
