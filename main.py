"""
A multi-user academic result management system with role-based access control.
Supports admin and student roles with secure login and CRUD operations.
"""

import mysql.connector
from mysql.connector import Error
from auth import login, hash_password
from admin import admin_menu
from student import student_menu
from db import get_connection

def main():
    print("=" * 50)
    print("   Student Result Management System")
    print("=" * 50)

    while True:
        print("\n1. Login")
        print("2. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            user = login(username, password)
            if user:
                print(f"\nWelcome, {user['username']}! Role: {user['role'].upper()}")
                if user["role"] == "admin":
                    admin_menu(user)
                elif user["role"] == "student":
                    student_menu(user)
            else:
                print("Invalid credentials. Please try again.")

        elif choice == "2":
            print("Goodbye")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
