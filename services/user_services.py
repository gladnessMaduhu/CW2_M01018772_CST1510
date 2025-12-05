import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user


def register_user(username, password, role="user"):
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, "Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(filepath="DATA/users.txt"):
    conn = connect_database()
    cursor = conn.cursor()
    path = Path(filepath)

    if not path.exists():
        return

    with open(path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                username, password_hash = parts[0], parts[1]
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, "user")
                )
    conn.commit()
    conn.close()