import sqlite3
from pathlib import Path
import hashlib

# DATABASE LOCATION  (always points to project root)
DB_PATH = Path(__file__).resolve().parent.parent / "users.db"

# CONNECT TO DATABASE
def connect_database():
    return sqlite3.connect(DB_PATH)

# CREATE TABLES

def create_tables():
    conn = connect_database()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


# PASSWORD HASHING
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ADD NEW USER
def add_user(username: str, password: str, email: str = None):
    conn = connect_database()
    cur = conn.cursor()

    hashed_pw = hash_password(password)

    try:
        cur.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_pw, email),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # username already exists
    finally:
        conn.close()

# GET USER BY USERNAME

def get_user(username: str):
    conn = connect_database()
    cur = conn.cursor()

    cur.execute("SELECT id, username, password, email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()
    return row

# RUN ONCE TO INITIALIZE DB

if __name__ == "__main__":
    create_tables()
    print(f"Database initialized at: {DB_PATH}")
