import sqlite3

# Connect to database
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    department TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollment (
    enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    marks INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

conn.commit()

# Functions
def add_student():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    dept = input("Enter department: ")
    
    cursor.execute("INSERT INTO students (name, age, department) VALUES (?, ?, ?)", (name, age, dept))
    conn.commit()
    print("Student added!")

def add_course():
    cname = input("Enter course name: ")
    cursor.execute("INSERT INTO courses (course_name) VALUES (?)", (cname,))
    conn.commit()
    print("Course added!")

def enroll_student():
    sid = int(input("Enter student ID: "))
    cid = int(input("Enter course ID: "))
    
    cursor.execute("INSERT INTO enrollment (student_id, course_id, marks) VALUES (?, ?, ?)", (sid, cid, 0))
    conn.commit()
    print("Student enrolled!")

def add_marks():
    sid = int(input("Enter student ID: "))
    cid = int(input("Enter course ID: "))
    marks = int(input("Enter marks: "))
    
    cursor.execute("""
    UPDATE enrollment
    SET marks = ?
    WHERE student_id = ? AND course_id = ?
    """, (marks, sid, cid))
    
    conn.commit()
    print("Marks updated!")

def view_report():
    sid = int(input("Enter student ID: "))
    
    cursor.execute("""
    SELECT students.name, courses.course_name, enrollment.marks
    FROM enrollment
    JOIN students ON students.student_id = enrollment.student_id
    JOIN courses ON courses.course_id = enrollment.course_id
    WHERE students.student_id = ?
    """, (sid,))
    
    records = cursor.fetchall()
    
    print("\n--- Report ---")
    for row in records:
        print("Name:", row[0], "| Course:", row[1], "| Marks:", row[2])

# Menu
while True:
    print("\n1. Add Student")
    print("2. Add Course")
    print("3. Enroll Student")
    print("4. Add Marks")
    print("5. View Report")
    print("6. Exit")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        add_student()
    elif choice == "2":
        add_course()
    elif choice == "3":
        enroll_student()
    elif choice == "4":
        add_marks()
    elif choice == "5":
        view_report()
    elif choice == "6":
        break
    else:
        print("Invalid choice!")

conn.close()
