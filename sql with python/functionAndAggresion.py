import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

#1
print("Count total number of students")
cursor.execute('SELECT COUNT(*) FROM students')
result = cursor.fetchall()
print(result)

#2
print("Average marks of students")
cursor.execute('SELECT AVG(marks) FROM students')
result = cursor.fetchall()
print(result)

#3
print("Highest and Lowest makrs")
cursor.execute('SELECT MAX(marks),MIN(marks) FROM students')
result = cursor.fetchall()
print(result)

#4
print("department-wise average marks")
cursor.execute('SELECT department,AVG(marks) FROM students GROUP BY department')
result = cursor.fetchall()
print(result)

#5
print("department where average marks>70")
cursor.execute('SELECT department,AVG(marks) FROM students GROUP BY department HAVING AVG(marks)>70')
result = cursor.fetchall()
print(result)