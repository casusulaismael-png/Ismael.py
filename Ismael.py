import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    year_level TEXT NOT NULL
)
""")
conn.commit()


MENU_TEXT = """
========================================
       STUDENT MANAGEMENT SYSTEM
========================================
1. Add Student       (Create)
2. View Students     (Read)
3. Update Student    (Update)
4. Delete Student    (Delete)
5. Exit
========================================
"""


# CREATE - Add a new student
def add_student():
    print("\n--- ADD NEW STUDENT ---")

    name = input("Enter student name: ").strip()
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    course = input("Enter course: ").strip()
    if not course:
        print("[ERROR] Course cannot be empty.")
        return

    year = input("Enter year level: ").strip()
    if not year:
        print("[ERROR] Year level cannot be empty.")
        return

    cursor.execute("""
        INSERT INTO students (name, course, year_level)
        VALUES (?, ?, ?)
    """, (name, course, year))

    conn.commit()
    print("[SUCCESS] Student added successfully!")


# READ - View all students
def view_students():
    print("\n--- STUDENT LIST ---")

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if not records:
        print("No student records found.")
        return

    for student in records:
        print("--------------------------------")
        print("Student ID:", student[0])
        print("Name:", student[1])
        print("Course:", student[2])
        print("Year Level:", student[3])


# UPDATE - Update student information
def update_student():
    print("\n--- UPDATE STUDENT ---")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("[ERROR] Invalid student ID.")
        return

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()

    if student is None:
        print("[ERROR] Student not found.")
        return

    name = input("Enter new name: ").strip()
    course = input("Enter new course: ").strip()
    year = input("Enter new year level: ").strip()

    if not name or not course or not year:
        print("[ERROR] All fields are required.")
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, course = ?, year_level = ?
        WHERE student_id = ?
    """, (name, course, year, student_id))

    conn.commit()
    print("[SUCCESS] Student updated successfully!")


# DELETE - Remove a student
def delete_student():
    print("\n--- DELETE STUDENT ---")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("[ERROR] Invalid student ID.")
        return

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print("[ERROR] Student not found.")
        return

    confirm = input("Are you sure you want to delete? (yes/no): ")

    if confirm.lower() == "yes":
        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        conn.commit()
        print("[SUCCESS] Student deleted successfully!")
    else:
        print("Deletion cancelled.")


# MAIN PROGRAM
while True:
    print(MENU_TEXT)

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("Thank you for using Student Management System!")
        break

    else:
        print("[ERROR] Invalid choice. Please try again.")

conn.close()
