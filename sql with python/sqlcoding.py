import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS employees1')
cursor.execute('DROP TABLE IF EXISTS employees2')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees1(
                id INT PRIMARY KEY,
                name VARCHAR(50),
                salary INT,
                dept TEXT,
                hire_date DATE
    )
    ''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees2(
                id INT PRIMARY KEY,
                name VARCHAR(50),
                salary INT
    )
    ''')
cursor.executemany("INSERT INTO employees1 VALUES (?, ?, ?, ?, ?)", [
    (1, 'Alice',   90000, 'HR',      '2024-01-15'),
    (2, 'Bob',     75000, 'IT',      '2023-06-20'),
    (3, 'Charlie', 90000, 'IT',      '2022-03-10'),
    (4, 'Diana',   60000, 'HR',      '2025-01-05'),
    (5, 'Eve',     85000, 'Finance', '2024-11-30'),
    (6, 'Frank',   75000, 'Finance', '2023-08-14'),
    (7, 'Grace',   60000, 'IT',      '2025-02-20'),
])

cursor.executemany("INSERT INTO employees2 VALUES (?, ?, ?)", [
    (3, 'Charlie', 90000),
    (5, 'Eve',     85000),
    (8, 'Henry',   50000),
])

conn.commit()

print("Write query to find Nth highest salary")

n = 3
cursor.execute('SELECT DISTINCT salary FROM employees1 ORDER BY salary DESC LIMIT 1 OFFSET ?', (n - 1,))
for row in cursor.fetchall():
    print(row)

print("Remove duplicate recods ")
cursor.execute('SELECT DISTINCT name FROM employees1')
for row in cursor.fetchall():
    print(row)

print("find records common in two tables")
cursor.execute('SELECT name FROM employees1 INTERSECT SELECT name FROM employees2')
for row in cursor.fetchall():
    print(row)

print("find employess hired in last 6 months")
cursor.execute('SELECT name FROM employees1 WHERE hire_date >= date("now", "-6 months")')
for row in cursor.fetchall():
    print(row)

print("find continuous duplicate values")
cursor.execute('SELECT name FROM (SELECT name, LAG(name) OVER (ORDER BY id) AS prev_name FROM employees1) WHERE name = prev_name')
for row in cursor.fetchall():
    print(row)
