# admin.py — Admin role operations
# Roles includes: manage students, courses, grades, and view reports.

from db import get_connection, close
from auth import hash_password

def add_student(name: str, email: str, username: str, password: str):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Add to users table
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'student')",
            (username, hash_password(password)),
        )
        user_id = cursor.lastrowid

        # Add to students table
        cursor.execute(
            "INSERT INTO students (user_id, name, email) VALUES (%s, %s, %s)",
            (user_id, name, email),
        )
        conn.commit()
        print(f"Student '{name}' added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[Error] {e}")
    finally:
        close(conn, cursor)


def view_all_students():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT s.student_id, s.name, s.email, u.username
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            ORDER BY s.student_id
            """
        )
        rows = cursor.fetchall()
        if not rows:
            print("No students found.")
            return
        print(f"\n{'ID':<5} {'Name':<20} {'Email':<30} {'Username':<15}")
        print("-" * 72)
        for r in rows:
            print(f"{r['student_id']:<5} {r['name']:<20} {r['email']:<30} {r['username']:<15}")
    finally:
        close(conn, cursor)


def delete_student(student_id: int):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Get linked user_id first
        cursor.execute("SELECT user_id FROM students WHERE student_id = %s", (student_id,))
        row = cursor.fetchone()
        if not row:
            print("Student not found.")
            return
        user_id = row[0]
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        print("Student deleted.")
    except Exception as e:
        conn.rollback()
        print(f"[Error] {e}")
    finally:
        close(conn, cursor)

def add_course(course_name: str, course_code: str, credits: int):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO courses (course_name, course_code, credits) VALUES (%s, %s, %s)",
            (course_name, course_code, credits),
        )
        conn.commit()
        print(f"Course '{course_name}' added.")
    except Exception as e:
        conn.rollback()
        print(f"[Error] {e}")
    finally:
        close(conn, cursor)


def view_all_courses():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM courses ORDER BY course_id")
        rows = cursor.fetchall()
        if not rows:
            print("No courses found.")
            return
        print(f"\n{'ID':<5} {'Code':<10} {'Name':<30} {'Credits':<8}")
        print("-" * 55)
        for r in rows:
            print(f"{r['course_id']:<5} {r['course_code']:<10} {r['course_name']:<30} {r['credits']:<8}")
    finally:
        close(conn, cursor)

def assign_grade(student_id: int, course_id: int, marks: float, grade: str):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO results (student_id, course_id, marks, grade)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE marks = %s, grade = %s
            """,
            (student_id, course_id, marks, grade, marks, grade),
        )
        conn.commit()
        print("Grade assigned successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[Error] {e}")
    finally:
        close(conn, cursor)


def view_all_results():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT s.name AS student, c.course_name, c.course_code,
                   r.marks, r.grade
            FROM results r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            ORDER BY s.name, c.course_name
            """
        )
        rows = cursor.fetchall()
        if not rows:
            print("No results found.")
            return
        print(f"\n{'Student':<20} {'Course':<25} {'Code':<10} {'Marks':<8} {'Grade':<6}")
        print("-" * 72)
        for r in rows:
            print(f"{r['student']:<20} {r['course_name']:<25} {r['course_code']:<10} {r['marks']:<8} {r['grade']:<6}")
    finally:
        close(conn, cursor)

def admin_menu(user):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Delete Student")
        print("4. Add Course")
        print("5. View All Courses")
        print("6. Assign / Update Grade")
        print("7. View All Results")
        print("8. Logout")

        choice = input("Choice: ").strip()

        if choice == "1":
            name     = input("Student Name: ").strip()
            email    = input("Email: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            add_student(name, email, username, password)

        elif choice == "2":
            view_all_students()

        elif choice == "3":
            sid = int(input("Student ID to delete: "))
            delete_student(sid)

        elif choice == "4":
            cname = input("Course Name: ").strip()
            ccode = input("Course Code: ").strip()
            cred  = int(input("Credits: "))
            add_course(cname, ccode, cred)

        elif choice == "5":
            view_all_courses()

        elif choice == "6":
            sid    = int(input("Student ID: "))
            cid    = int(input("Course ID: "))
            marks  = float(input("Marks: "))
            grade  = input("Grade (A/B/C/D/F): ").strip().upper()
            assign_grade(sid, cid, marks, grade)

        elif choice == "7":
            view_all_results()

        elif choice == "8":
            print("Logged out.")
            break

        else:
            print("Invalid choice.")
