import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS customers')
cursor.execute('DROP TABLE IF EXISTS orders')

cursor.execute('''CREATE TABLE customers(
               customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
               )
''')

cursor.execute('''CREATE TABLE orders(
               order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                amount REAL
                )
''')

cursor.execute("INSERT OR IGNORE INTO customers (name) VALUES ('Alice')")
cursor.execute("INSERT OR IGNORE INTO customers (name) VALUES ('Bob')")   
cursor.execute("INSERT OR IGNORE INTO orders (customer_id, amount) VALUES (1, 100.0)")
cursor.execute("INSERT OR IGNORE INTO orders (customer_id, amount) VALUES (1, 150.0)")
cursor.execute("INSERT OR IGNORE INTO orders (customer_id, amount) VALUES (2, 200.0)")

print("TASK1: add index to improve search on orders.customer_id")
cursor.execute("CREATE INDEX idx_customer_id ON orders(customer_id)")
print("index created on orders.customer_id\n")

print("TASK2: use EXPLAIN to analyze query")
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1")
for row in cursor.fetchall():
    print(row)

print("\nTASK3: Optimize a slow join query")
cursor.execute('''SELECT customers.name, orders.amount
                  FROM customers
                  JOIN orders ON customers.customer_id = orders.customer_id
                  WHERE orders.amount > 150''')
for row in cursor.fetchall():
    print(row)

print("\nTASK4: Explain when index should not be used")
print("Indexes may not be used when the query is expected to return a large portion of the table,")
print("or when the query involves complex expressions that cannot utilize the index effectively.")
print("In such cases, the database optimizer may choose a full table scan instead of using the index.") 
conn.close()