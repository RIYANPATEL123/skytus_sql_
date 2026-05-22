import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT,
        amount REAL
    );
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        price REAL
    );
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    );

    INSERT INTO customers (name, city) VALUES
        ('Alice', 'Mumbai'), ('Bob', 'Delhi'),
        ('Charlie', 'Mumbai'), ('Diana', 'Pune'), ('Eve', 'Delhi');

    INSERT INTO products (product_name, price) VALUES
        ('Laptop', 55000), ('Phone', 25000), ('Headphones', 3000);

    INSERT INTO orders (customer_id, order_date, amount) VALUES
        (1, '2024-01-15', 55000), (1, '2024-02-20', 25000),
        (2, '2024-01-10', 18000), (3, '2024-03-05', 58000),
        (5, '2024-02-28', 56500);

    INSERT INTO order_items (order_id, product_id, quantity) VALUES
        (1, 1, 1), (2, 2, 1), (3, 2, 1),
        (4, 1, 1), (5, 1, 1);
""")

#1
print("\n Total orders per customer")
cursor.execute('SELECT c.name,COUNT(o.order_id) FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id ORDER BY c.customer_id')
for row in cursor.fetchall():
    print(row)

#2
print("\n Customers who never placed an order")
cursor.execute('SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id WHERE o.order_id is NULL ')
for row in cursor.fetchall():
    print(row)

#3
print("\n Highest selling product")
cursor.execute("""
    SELECT p.product_name, SUM(oi.quantity)
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY oi.product_id
    ORDER BY SUM(oi.quantity) DESC
    LIMIT 1
""")
for row in cursor.fetchall():
    print(row)

#4
print("\n Monthly Sales report")
cursor.execute("""
    SELECT strftime('%Y-%m', order_date), COUNT(*), SUM(amount)
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
""")
for row in cursor.fetchall():
    print(row)


#5
print("\n Customers with total purchase > 50,000")
cursor.execute('''SELECT c.name, SUM(o.amount)
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    HAVING SUM(o.amount) > 50000''')
for row in cursor.fetchall():
    print(row)

#6
print("\n Top 3 cities by revenue")
cursor.execute('''SELECT c.name, SUM(o.amount)
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.city
    ORDER BY SUM(o.amount) DESC 
    LIMIT 3
               ''')
for row in cursor.fetchall():
    print(row)
