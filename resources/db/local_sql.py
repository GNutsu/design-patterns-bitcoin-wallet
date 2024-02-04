import os
import sqlite3

from definitions import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print(cursor.execute("SELECT * FROM USERS").fetchall())
print(cursor.execute("SELECT * FROM TRANSACTIONS").fetchall())
conn.close()
