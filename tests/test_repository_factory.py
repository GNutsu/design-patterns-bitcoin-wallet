from bitcoinwallet.core.repository.repository_factory import RepositoryFactory
from definitions import TEST_DB_NAME


class TestRepositoryFactory(RepositoryFactory):
    __test__ = False

    @staticmethod
    def get_db_path() -> str:
        return TEST_DB_NAME
