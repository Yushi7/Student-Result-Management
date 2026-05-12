# auth.py — Authentication with hashed passwords

import hashlib
from db import get_connection, close

def hash_password(password: str) -> str:
    """Return SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username: str, password: str):
    # Validate credentials against the database & returns user dict on success, None on failure.
    
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        hashed = hash_password(password)
        cursor.execute(
            "SELECT user_id, username, role FROM users WHERE username = %s AND password_hash = %s",
            (username, hashed),
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"[Auth Error] {e}")
        return None
    finally:
        close(conn, cursor)
