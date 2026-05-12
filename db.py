"""
db.py — Database connection handler
"""

import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "database": os.getenv("DB_NAME", "student_result_db"),
}


def get_connection():
    """Return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB Error] Could not connect: {e}")
        return None


def close(conn, cursor=None):
    """Safely close cursor and connection."""
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
