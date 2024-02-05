import os
import sqlite3

from definitions import DB_NAME


def db_setup(db_path: str) -> str:
    if not os.path.exists(db_path):
        open(db_path, "w").close()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            api_key PRIMARY KEY,
            wallet_count
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            id PRIMARY KEY,
            owner_api_key,
            balance,
            creation_time,
            address NOT NULL UNIQUE,
            FOREIGN KEY(owner_api_key) REFERENCES users(api_key)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id PRIMARY KEY,
            from_addr,
            to_addr,
            amount,
            fee_cost,
            transaction_time,
            FOREIGN KEY(from_addr) REFERENCES wallets(address),
            FOREIGN KEY(to_addr) REFERENCES wallets(address)
        )
    """
    )

    conn.commit()
    conn.close()

    return db_path


print(DB_NAME)
db_setup(DB_NAME)
