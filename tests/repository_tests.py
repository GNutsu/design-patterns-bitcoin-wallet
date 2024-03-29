import os
import uuid
from typing import Generator

import pytest

from bitcoinwallet.core.model.entity import TransactionEntity, UserEntity, WalletEntity
from bitcoinwallet.core.repository.repository import IRepository
from bitcoinwallet.core.util import datetime_now
from definitions import TEST_DB_NAME
from resources.db.sql import db_setup
from tests.test_repository_factory import TestRepositoryFactory


@pytest.fixture(scope="session")
def setup_test_db() -> Generator[None, None, None]:
    db_setup(TEST_DB_NAME)

    yield
    TestRepositoryFactory.get_instance().close_connections()

    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)


def test_user_repository(setup_test_db: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )

    api_key: str = str(uuid.uuid4())
    wallet_count: int = 0
    u: UserEntity = UserEntity(api_key, wallet_count)
    user_repo.create(u)

    user = user_repo.read(api_key)
    assert user and user == u

    wallet_count += 1
    u.wallet_count = wallet_count
    user_repo.update(u)

    user = user_repo.read(api_key)
    assert user and user == u

    another_api_key: str = str(uuid.uuid4())
    user_repo.create(UserEntity(another_api_key, wallet_count))

    users = user_repo.get_by_field("wallet_count", wallet_count)
    assert len(users) == 2

    user_repo.delete(api_key)
    users1 = user_repo.get_by_field("wallet_count", wallet_count)
    assert len(users1) == 1


def test_wallet_repository(setup_test_db: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )
    wallet_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        WalletEntity
    )

    api_key: str = str(uuid.uuid4())
    wallet_count: int = 0

    user_repo.create(UserEntity(api_key, wallet_count))

    wallet_id: str = str(uuid.uuid4())
    wallet_addr: str = str(uuid.uuid4())
    balance: int = 100000
    creation_time: str = datetime_now()
    w: WalletEntity = WalletEntity(
        wallet_id, api_key, balance, creation_time, wallet_addr
    )
    wallet_repo.create(w)

    wallet = wallet_repo.read(wallet_id)
    assert wallet and wallet == w

    balance += 100000
    w.balance = balance
    wallet_repo.update(w)

    wallet = wallet_repo.read(wallet_id)
    assert wallet and wallet == w

    another_wallet_id: str = str(uuid.uuid4())
    another_wallet_addr: str = str(uuid.uuid4())
    wallet_repo.create(
        WalletEntity(
            another_wallet_id, api_key, balance, datetime_now(), another_wallet_addr
        )
    )

    wallets = wallet_repo.get_by_field("owner_api_key", api_key)
    assert len(wallets) == 2

    wallet_repo.delete(another_wallet_id)

    wallets1 = wallet_repo.get_by_field("owner_api_key", api_key)
    assert len(wallets1) == 1


def test_transaction_repository(setup_test_db: str) -> None:
    user_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        UserEntity
    )
    wallet_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        WalletEntity
    )
    transaction_repo: IRepository = TestRepositoryFactory.get_instance().get_repository(
        TransactionEntity
    )

    user: UserEntity = UserEntity(str(uuid.uuid4()), 1)
    user_repo.create(user)
    wallet1: WalletEntity = WalletEntity(
        str(uuid.uuid4()), user.api_key, 1000000, datetime_now(), str(uuid.uuid4())
    )
    wallet2: WalletEntity = WalletEntity(
        str(uuid.uuid4()), user.api_key, 1000000, datetime_now(), str(uuid.uuid4())
    )
    wallet_repo.create(wallet1)
    wallet_repo.create(wallet2)

    tr1_id: str = str(uuid.uuid4())
    amount1: int = 10000
    fee1: int = 10
    time1: str = datetime_now()
    t1: TransactionEntity = TransactionEntity(
        tr1_id, wallet1.id, wallet2.id, amount1, fee1, time1
    )
    transaction_repo.create(t1)

    tr1 = transaction_repo.read(tr1_id)
    assert tr1 and tr1 == t1

    amount1 += 10000
    t1.amount = amount1
    transaction_repo.update(t1)

    tr1 = transaction_repo.read(tr1_id)
    assert tr1 and tr1 == t1

    tr2_id = str(uuid.uuid4())
    transaction_repo.create(
        TransactionEntity(tr2_id, wallet1.id, wallet2.id, amount1, fee1, datetime_now())
    )

    transactions = transaction_repo.get_by_field("from_addr", wallet1.id)
    assert len(transactions) == 2

    transaction_repo.delete(tr2_id)
    transactions1 = transaction_repo.get_by_field("from_addr", wallet1.id)
    assert len(transactions1) == 1
