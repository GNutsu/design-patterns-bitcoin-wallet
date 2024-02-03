import sqlite3

#
# #
DATABASE_PATH = "bw_db.db"
#
con = sqlite3.connect(DATABASE_PATH)
cur = con.cursor()

# Creating
# cur.execute("CREATE TABLE USERS(api_key, wallet_count)")
# cur.execute("CREATE TABLE WALLETS(address, owner_api_key, satoshi_balance)")
# cur.execute("""CREATE TABLE TRANSACTIONS(id, from_addr,
# to_addr, amount, fee_cost, transaction_time)""")
#
# con.commit()

# DROPPING
# cur.execute("DROP TABLE USERS")
# cur.execute("DROP TABLE WALLETS")
# cur.execute("DROP TABLE TRANSACTIONS")

print(cur.execute("SELECT * FROM USERS").fetchall())
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchall())

print(cur.execute("SELECT * FROM USERS").fetchall())
print(cur.execute("SELECT * FROM TRANSACTIONS").fetchall())
