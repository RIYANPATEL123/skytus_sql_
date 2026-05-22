import sqlite3

conn = sqlite3.connect("store.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product TEXT NOT NULL,
        amount REAL NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_email
    ON users(email)
""")

cursor.execute("""
    CREATE VIEW IF NOT EXISTS user_order_summary AS
    SELECT
        u.id AS user_id,
        u.email AS user_email,
        COUNT(o.id) AS total_orders,
        SUM(o.amount) AS total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.email
""")

conn.commit()
print("All tasks completed successfully!")

cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", ("hello@gmail.com", "hello123"))
cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", ("world@gmail.com","world123"))

cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", (1, "Book",500))
cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", (1, "Pen", 100))
cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)", (2, "Bag",2000))

conn.commit()

print("\n User Order Summary ")
for row in cursor.execute("SELECT * FROM user_order_summary"):
    print(row)

conn.close()