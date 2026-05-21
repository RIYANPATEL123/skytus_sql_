import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS students')

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
    (4,'Jessica',101,79000),
    (5,'Harvey',103,84000),
    (6,'Mike',None,40000),
]

cursor.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?)',employees)
conn.commit()

#1
print("\nEmployee name with department name")
cursor.execute('SELECT emp_name,dept_name FROM employees JOIN departments ON employees.dept_id = departments.dept_id')
for row in cursor.fetchall():
    print(row)



#2
print("\nemployees earning more thatn 50,000")
cursor.execute('SELECT salary,emp_name FROM employees WHERE salary>50000')
for row in cursor.fetchall():
    print(row)


#3
print("\ndepartment-wise total salary")
cursor.execute('SELECT dept_name,SUM(salary) FROM employees JOIN departments ON employees.dept_id = departments.dept_id GROUP BY dept_name')
for row in cursor.fetchall():
    print(row)


#4
print("\nDepartments with more than 2 employees:")
cursor.execute('SELECT dept_name, COUNT(*) FROM employees JOIN departments ON employees.dept_id = departments.dept_id GROUP BY dept_name HAVING COUNT(*) > 2')
for row in cursor.fetchall():
    print(row)

#5
print("\n Employees without a department:")
cursor.execute('SELECT emp_name FROM employees WHERE dept_id IS NULL')
for row in cursor.fetchall():
    print(row[0])