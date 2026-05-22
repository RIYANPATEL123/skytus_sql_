import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        holder_name TEXT NOT NULL,
        balance     REAL NOT NULL CHECK(balance >= 0)
    )
""")
conn.commit()


#1
conn.execute("BEGIN")
print("Transaction started.")


#2
print("\nInsert record into accounts")
cursor.execute("INSERT INTO accounts (holder_name, balance) VALUES (?, ?)", ("hello",80000))
cursor.execute("INSERT INTO accounts (holder_name, balance) VALUES (?, ?)", ("world",50000))
cursor.execute("INSERT INTO accounts (holder_name, balance) VALUES (?, ?)", ("this", 30000))
conn.commit()
print("\n records sucessfully added")


#3
print("\nRollback changes")
try:
    conn.execute("BEGIN")
    cursor.execute("UPDATE accounts SET balance = balance - 5000 WHERE holder_name = 'hello'")
    cursor.execute("INSERT INTO accounts (holder_name, balance) VALUES (?, ?)", ("Invalid", -9999))
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Rolled back: {e}")


#4
print("\n Commit valid tarnsactions")
conn.execute("BEGIN")
cursor.execute("INSERT INTO accounts (holder_name, balance) VALUES (?, ?)", ("riyan", 150000))
conn.commit()


#5
print("\nDemonstrate transfer of money using transaction")
def transfer(from_id, to_id, amount):
    cursor.execute("SELECT holder_name, balance FROM accounts WHERE account_id = ?", (from_id,))
    sender = cursor.fetchone()
    cursor.execute("SELECT holder_name, balance FROM accounts WHERE account_id = ?", (to_id,))
    receiver = cursor.fetchone()

    if sender[1] < amount:
        print(f"Insufficient funds. {sender[0]} has ₹{sender[1]:,.2f}")
        return

    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, from_id))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, to_id))
    conn.commit()
    print(f"₹{amount:,.2f} transferred from {sender[0]} to {receiver[0]}")

transfer(1, 2, 20000)
transfer(3, 1, 99999)

conn.close()