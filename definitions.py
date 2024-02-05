import os

BITCOIN_FEE_PERCENTAGE = 1.5
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(ROOT_PATH, "resources", "db", "bw_db.db")
TEST_DB_NAME = os.path.join(ROOT_PATH, "tests", "bw_db.db")

FORMAT = "%Y-%m-%d %H:%M:%S.%f"

MAX_WALLETS_PER_USER = 3
INITIAL_WALLET_BALANCE = 100000000

GECKO_CURRENCY_BASE_URL = "https://api.coingecko.com/api/v3/simple/price"
CACHE_TTL = 300
CURRENCY_CACHE_MAX_SIZE = 1
