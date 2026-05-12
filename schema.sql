-- ============================================================
--  Student Result Management System — Database Schema
--  Database: student_result_db
--  Normal Form: 3NF
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_result_db;
USE student_result_db;

-- ── Users (authentication) ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(64)  NOT NULL,          -- SHA-256 hex digest
    role          ENUM('admin', 'student') NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);

-- ── Students ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    student_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT          NOT NULL UNIQUE,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_email (email)
);

-- ── Courses ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    course_id   INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20)  NOT NULL UNIQUE,
    credits     TINYINT      NOT NULL CHECK (credits BETWEEN 1 AND 6),
    INDEX idx_course_code (course_code)
);

-- ── Results ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS results (
    result_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT            NOT NULL,
    course_id   INT            NOT NULL,
    marks       DECIMAL(5, 2)  NOT NULL CHECK (marks BETWEEN 0 AND 100),
    grade       CHAR(2)        NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_student_course (student_id, course_id),   -- one result per course per student
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)  ON DELETE CASCADE,
    INDEX idx_student (student_id)
);

-- ── Seed: Default Admin Account ───────────────────────────────────────────────
-- Password: admin123  (SHA-256 hash)
INSERT IGNORE INTO users (username, password_hash, role)
VALUES (
    'admin',
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
    'admin'
);

-- ── Sample Data ───────────────────────────────────────────────────────────────
INSERT IGNORE INTO courses (course_name, course_code, credits) VALUES
    ('Data Structures & Algorithms', 'CS201', 4),
    ('Database Management Systems',  'CS301', 3),
    ('Operating Systems',            'CS302', 3),
    ('Machine Learning',             'CS401', 4),
    ('Computer Networks',            'CS303', 3);
