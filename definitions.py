import os

BITCOIN_FEE_PERCENTAGE = 1.5
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(ROOT_PATH, "resources", "db", "bw_db.db")
TEST_DB_NAME = "test_db.db"

FORMAT = "%Y-%m-%d %H:%M:%S.%f"
