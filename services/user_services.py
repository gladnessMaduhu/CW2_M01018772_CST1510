import sqlite3
from pathlib import Path
import bcrypt
from app.data.db import connect_database
# 1. Migrate users from users.txt
def migrate_users_from_file(conn, filepath):
    """
    Migrate users from users.txt to the database.

    Args:
        conn: Database connection
        filepath: Path to users.txt
    """
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        print("   No users to migrate.")
        return

    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash
            parts = line.split(",")
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, "user")
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f"Migrated {migrated_count} users from {Path(filepath).name}")


# -----------------------------
# 2. Register a new user
# -----------------------------
def register_user(conn, username, password, role="user"):
    """
    Register a new user in the database.

    Args:
        conn: SQLite database connection
        username: User's login name
        password: Plain text password
        role: User role (default: 'user')

    Returns:
        tuple: (success: bool, message: str)
    """
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return False, f"Username '{username}' already exists."

    # Hash the password
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode("utf-8")

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    return True, f"User '{username}' registered successfully!"


# 3. Login user

def login_user(conn, username, password):
    """
    Authenticate a user against the database.

    Args:
        conn: SQLite database connection
        username: User's login name
        password: Plain text password to verify

    Returns:
        tuple: (success: bool, message: str)
    """
    cursor = conn.cursor()

    # Fetch user record (only password_hash)
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        return False, "Username not found."

    stored_hash = row[0].encode('utf-8')
    password_bytes = password.encode('utf-8')

    # Verify password using bcrypt
    if bcrypt.checkpw(password_bytes, stored_hash):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."
