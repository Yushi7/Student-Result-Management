# Student Result Management System

A multi-user academic result management system built with **Python** and **MySQL**. Supports two roles — **Admin** and **Student** — with secure login, role-based access control, and a 3NF-normalized relational database.

---

## Features

### Admin
- Add, view, and delete student accounts
- Add and view courses
- Assign and update grades for any student
- View all results across all students and courses

### Student
- View personal results with average marks
- View own profile

### Security
- Passwords stored as SHA-256 hashes (never plain text)
- Role-based access: students cannot access admin operations
- Indexed queries for faster lookups

---

## Project Structure

```
student-result-management/
├── main.py          # Entry point, login flow
├── auth.py          # Authentication & password hashing
├── db.py            # MySQL connection handler
├── admin.py         # Admin operations & menu
├── student.py       # Student operations & menu
├── schema.sql       # Database schema (3NF) + seed data
├── requirements.txt
└── README.md
```

---

## Database Schema

```
users ──────────── students ──────── results ──────── courses
(user_id, role)    (student_id,      (student_id,     (course_id,
                    user_id,          course_id,        course_name,
                    name, email)      marks, grade)     course_code,
                                                        credits)
```

All tables satisfy **Third Normal Form (3NF)**:
- No partial dependencies
- No transitive dependencies
- Foreign key constraints enforce referential integrity

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Yushi7/student-result-management.git
cd student-result-management
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure the database**

Open `db.py` and update the credentials, or set environment variables:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=student_result_db
```

**4. Create the database and tables**
```bash
mysql -u root -p < schema.sql
```

**5. Run the application**
```bash
python main.py
```

---

## Default Login

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |

> Change the admin password after first login.

---

## Sample Workflow

```
===  Student Result Management System  ===

1. Login
2. Exit
Enter choice: 1
Username: admin
Password: ********

Welcome, admin! Role: ADMIN

--- Admin Menu ---
1. Add Student
2. View All Students
3. Delete Student
4. Add Course
5. View All Courses
6. Assign / Update Grade
7. View All Results
8. Logout
```

---

## Technologies Used

| Layer       | Technology              |
|-------------|-------------------------|
| Language    | Python 3                |
| Database    | MySQL 8                 |
| DB Driver   | mysql-connector-python  |
| Auth        | SHA-256 (hashlib)       |

---

## Key Concepts Demonstrated

- **3NF Database Design** — normalized schema with no redundancy
- **Role-Based Access Control** — admin vs student permissions enforced at application level
- **Indexed Queries** — indexes on `username`, `email`, `student_id` for faster lookups
- **Prepared Statements** — parameterized queries to prevent SQL injection
- **Referential Integrity** — `ON DELETE CASCADE` foreign keys

---

## Author

**Ayushi Nishita Ekka**  
BIT Mesra — CSE, 2023–2027  
[GitHub](https://github.com/Yushi7) | [LinkedIn](https://www.linkedin.com/in/ayushi-nishita-ekka-81340b2a6/)
