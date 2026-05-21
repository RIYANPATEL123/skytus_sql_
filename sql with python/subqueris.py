import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS employees(
               emp_id INT PRIMARY KEY,
               emp_name VARCHAR(50),
               dept_id INT,
               salary INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS departments(
               dept_id INT PRIMARY KEY,
               dept_name VARCHAR(50)
               )
''')

departments =[
    (101,'IT'),
    (102,'SALES'),
    (103,'ACC'),
]

cursor.executemany('INSERT OR IGNORE INTO departments VALUES (?,?)',departments)

employees = [
    (1,'HELLO',101,10000),
    (2,'World',102,90000),
    (3,'TEam',101,64000),
    (4,'Amit',101,79000),
    (5,'Harvey',103,84000),
    (6,'Mike',None,40000),
]

cursor.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?)',employees)
conn.commit()

print("\nFind employees earning more than average salary")
cursor.execute('SELECT emp_name,AVG(salary) FROM employees WHERE salary>(SELECT AVG(salary) FROM employees)')
for row in cursor.fetchall():
    print(row)


print("\nFind department with highest total salary")
cursor.execute('''
SELECT dept_name, SUM(salary) as total_salary
FROM employees 
JOIN departments ON employees.dept_id = departments.dept_id 
GROUP BY dept_name 
ORDER BY total_salary
LIMIT 1
''')
for row in cursor.fetchall():
    print(row)


print("\nDisplay employee with second highest salary")
cursor.execute('''SELECT emp_name, salary 
FROM employees 
ORDER BY salary DESC 
LIMIT 1 OFFSET 1
''')
for row in cursor.fetchall():
    print(row)


print("\nemployees working in same department as 'Amit'")
cursor.execute('''SELECT emp_name 
FROM employees 
WHERE dept_id = (SELECT dept_id FROM employees WHERE emp_name = 'Amit')
AND emp_name != 'Amit Kumar'
''')
for row in cursor.fetchall():
    print(row)