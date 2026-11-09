
import mysql.connector

# STUDENT MANAGEMENT SYSTEM 
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )


# CREATE DATABASE AND TABLE
def setup_database():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS students_db")
    cursor.execute("USE students_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            course VARCHAR(100),
            year_level VARCHAR(30),
            section VARCHAR(50)
        )
    """)

    db.commit()
    cursor.close()
    db.close()


# ADD STUDENT
def add_student():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("USE students_db")

    print("\n--- ADD STUDENT ---")

    student_id = input("Student ID: ")
    name = input("Full Name: ")
    age = int(input("Age: "))
    course = input("Course: ")
    year = input("Year Level: ")
    section = input("Section: ")

    query = """
    INSERT INTO students
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        student_id, name, age,
        course, year, section
    ))

    db.commit()
    print("\nStudent added successfully!")

    cursor.close()
    db.close()


# VIEW STUDENTS
def view_students():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("USE students_db")

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    print("\n--- STUDENT LIST ---")

    if not records:
        print("No student records found.")

    for student in records:
        print("\nStudent ID:", student[0])
        print("Name:", student[1])
        print("Age:", student[2])
        print("Course:", student[3])
        print("Year Level:", student[4])
        print("Section:", student[5])
        print("----------------------")

    cursor.close()
    db.close()


# UPDATE STUDENT
def update_student():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("USE students_db")

    print("\n--- UPDATE STUDENT ---")

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (student_id,)
    )

    if cursor.fetchone() is None:
        print("Student not found!")
    else:
        name = input("New Name: ")
        age = int(input("New Age: "))
        course = input("New Course: ")
        year = input("New Year Level: ")
        section = input("New Section: ")

        query = """
        UPDATE students
        SET name=%s, age=%s, course=%s,
            year_level=%s, section=%s
        WHERE student_id=%s
        """

        cursor.execute(query, (
            name, age, course, year,
            section, student_id
        ))

        db.commit()
        print("Student updated successfully!")

    cursor.close()
    db.close()


# DELETE STUDENT
def delete_student():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("USE students_db")

    print("\n--- DELETE STUDENT ---")

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (student_id,)
    )

    if cursor.fetchone() is None:
        print("Student not found!")
    else:
        confirm = input("Confirm delete? (yes/no): ")

        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM students WHERE student_id=%s",
                (student_id,)
            )
            db.commit()
            print("Student deleted successfully!")
        else:
            print("Delete cancelled.")

    cursor.close()
    db.close()


# MAIN MENU
def main():
    setup_database()

    while True:
        print("\n================================")
        print("     STUDENT MANAGEMENT SYSTEM")
        print("================================")
        print("[1] Add Student")
        print("[2] View Students")
        print("[3] Update Student")
        print("[4] Delete Student")
        print("[5] Exit")
        print("================================")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                add_student()

            elif choice == "2":
                view_students()

            elif choice == "3":
                update_student()

            elif choice == "4":
                delete_student()

            elif choice == "5":
                print("Thank you for using the system!")
                break

            else:
                print("Invalid choice! Try again.")

        except mysql.connector.Error as error:
            print("Database Error:", error)

        except ValueError:
            print("Please enter a valid number for age.")


if __name__ == "__main__":
    try:
        main()
    except mysql.connector.Error as error:
        print("Unable to connect to MySQL:", error)
