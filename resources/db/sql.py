import os
import sqlite3


def db_setup(db_path: str) -> str:
    if not os.path.exists(db_path):
        open(db_path, "w").close()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            api_key TEXT PRIMARY KEY,
            wallet_count
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY,
            owner_api_key,
            balance,
            creation_time,
            FOREIGN KEY(owner_api_key) REFERENCES users(api_key)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            from_addr,
            to_addr,
            amount,
            fee_cost,
            transaction_time,
            FOREIGN KEY(from_addr) REFERENCES wallets(id),
            FOREIGN KEY(to_addr) REFERENCES wallets(id)
        )
    """
    )

    conn.commit()
    conn.close()

    return db_path


db_setup("bw_db.db")
