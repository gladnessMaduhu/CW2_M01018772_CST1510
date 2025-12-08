import sqlite3
from pathlib import Path
DB_PATH = Path("users.db")

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))