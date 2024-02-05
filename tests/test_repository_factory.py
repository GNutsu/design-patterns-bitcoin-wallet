from bitcoinwallet.core.repository.repository_factory import RepositoryFactory
from definitions import TEST_DB_NAME


class TestRepositoryFactory(RepositoryFactory):
    @staticmethod
    def get_db_path() -> str:
        return TEST_DB_NAME
