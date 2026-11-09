
import sqlite3

# DATABASE CONNECTION
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT,
    age INTEGER,
    course TEXT,
    year_level TEXT
)
""")

conn.commit()


# ADD STUDENT
def add_student():
    print("\n===== ADD STUDENT =====")

    student_id = input("Student ID: ")
    name = input("Student Name: ")
    age = int(input("Age: "))
    course = input("Course: ")
    year_level = input("Year Level: ")

    try:
        cursor.execute("""
        INSERT INTO students
        (student_id, name, age, course, year_level)
        VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, age, course, year_level))

        conn.commit()
        print("\nStudent added successfully!")

    except sqlite3.IntegrityError:
        print("\nStudent ID already exists!")


# VIEW STUDENT
def view_student():
    print("\n===== STUDENT LIST =====")

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
    else:
        for student in students:
            print("--------------------------------")
            print("ID:", student[0])
            print("Student ID:", student[1])
            print("Name:", student[2])
            print("Age:", student[3])
            print("Course:", student[4])
            print("Year Level:", student[5])


# UPDATE STUDENT
def update_student():
    print("\n===== UPDATE STUDENT =====")

    student_id = input("Enter Student ID: ")

    name = input("New Name: ")
    age = int(input("New Age: "))
    course = input("New Course: ")
    year_level = input("New Year Level: ")

    cursor.execute("""
    UPDATE students
    SET name=?, age=?, course=?, year_level=?
    WHERE student_id=?
    """, (name, age, course, year_level, student_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("\nStudent updated successfully!")
    else:
        print("\nStudent not found!")


# DELETE STUDENT
def delete_student():
    print("\n===== DELETE STUDENT =====")

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("\nStudent deleted successfully!")
    else:
        print("\nStudent not found!")


# MAIN MENU
while True:

    print("\n================================")
    print("    STUDENT MANAGEMENT SYSTEM")
    print("================================")
    print("[1] Add Student")
    print("[2] View Student")
    print("[3] Update Student")
    print("[4] Delete Student")
    print("[5] Exit")
    print("================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_student()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("\nThank you for using the system!")
        conn.close()
        break

    else:
        print("\nInvalid choice! Please try again.")
          
