"""
student.py — Student role operations
Students can view their own results and profile only.
"""

from db import get_connection, close

def get_student_id(user_id: int):
    """Fetch student_id from user_id."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id FROM students WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        close(conn, cursor)

def view_my_results(user_id: int):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    try:
        student_id = get_student_id(user_id)
        if not student_id:
            print("Student record not found.")
            return

        cursor.execute(
            """
            SELECT c.course_name, c.course_code, c.credits,
                   r.marks, r.grade
            FROM results r
            JOIN courses c ON r.course_id = c.course_id
            WHERE r.student_id = %s
            ORDER BY c.course_name
            """,
            (student_id,),
        )
        rows = cursor.fetchall()

        if not rows:
            print("No results available yet.")
            return

        print(f"\n{'Course':<28} {'Code':<10} {'Credits':<9} {'Marks':<8} {'Grade':<6}")
        print("-" * 65)
        total_marks = 0
        for r in rows:
            print(f"{r['course_name']:<28} {r['course_code']:<10} {r['credits']:<9} {r['marks']:<8} {r['grade']:<6}")
            total_marks += r["marks"]

        avg = total_marks / len(rows)
        print("-" * 65)
        print(f"{'Average Marks:':<50} {avg:.2f}")

    finally:
        close(conn, cursor)

def view_my_profile(user_id: int):
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
            WHERE s.user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        if row:
            print(f"\nStudent ID : {row['student_id']}")
            print(f"Name       : {row['name']}")
            print(f"Email      : {row['email']}")
            print(f"Username   : {row['username']}")
        else:
            print("Profile not found.")
    finally:
        close(conn, cursor)

def student_menu(user):
    while True:
        print("\n--- Student Menu ---")
        print("1. View My Results")
        print("2. View My Profile")
        print("3. Logout")

        choice = input("Choice: ").strip()

        if choice == "1":
            view_my_results(user["user_id"])
        elif choice == "2":
            view_my_profile(user["user_id"])
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
