import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS students')

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
    student_id INT,
    name VARCHAR(50),
    department VARCHAR(30),
    year INT,
    marks INT,
    UNIQUE(name, department)
)
''')

students = [
    (1, 'Alice Johnson', 'CSE', 2, 85),
    (2, 'Bob Smith', 'ECE', 3, 72),
    (3, 'Charlie Brown', 'CSE', 1, 90),
    (4, 'Diana Prince', 'ME', 4, 68),
    (5, 'Eve Anderson', 'CSE', 2, 78),
    (6, 'Frank Miller', 'ECE', 3, 82),
    (7, 'Grace Lee', 'CSE', 1, 95),
]

cursor.executemany('INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?)', students)
conn.commit()

#1
print("All Student records:")
cursor.execute('SELECT * FROM students')
for row in cursor.fetchall():
    print(row)

#2
print("Only name and department:")
cursor.execute('SELECT name, department FROM students')
for row in cursor.fetchall():
    print(row)

#3
print("Students with marks greater than 75:")
cursor.execute('SELECT * FROM students WHERE marks > 75')
for row in cursor.fetchall():
    print(row)

#4
print("Students from CSE department")
cursor.execute('SELECT * FROM students WHERE department="CSE"')
for row in cursor.fetchall():
    print(row)

#5
print("Sor students by marks(descending)")
cursor.execute('SELECT * FROM students ORDER BY marks DESC')
for row in cursor.fetchall():
    print(row)

#6
print("Display top 3 scorers")
cursor.execute('SELECT * FROM students ORDER BY marks DESC LIMIT 3')
for row in cursor.fetchall():
    print(row)

conn.close()
