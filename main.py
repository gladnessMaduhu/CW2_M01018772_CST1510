# main.py
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_services import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident

# -----------------------------
# Complete Database Setup
# -----------------------------
def setup_database_complete():
    conn = connect_database()
    create_all_tables(conn)

    # Migrate users (provide filepath if needed)
    try:
        migrated_count = migrate_users_from_file(conn, filepath="users.txt")
        print(f"Migrated {migrated_count} users from users.txt")
    except Exception as e:
        print(f" Error during migration: {e}")

    conn.close()
    print(f"Database setup complete at {DB_PATH.resolve()}")


# -----------------------------
# Demo Functions
# -----------------------------
def demo_user_auth(conn):
    print("\n**8 User Authentication Demo ***")
    username = "alice"
    password = "SecurePass123!"

    # Register user
    success, msg = register_user(conn, username, password, "analyst")
    print(msg)

    # Login user
    success, msg = login_user(conn, username, password)
    print(msg)


def demo_incidents_crud(conn):
    print("\n*** Incident CRUD Demo ***")
    # Insert
    incident_id = insert_incident(conn, "2024-11-05", "Phishing", "High", "Open",
                                  "Suspicious email detected", "alice")
    print(f"Created incident #{incident_id}")

    # Update
    rows_updated = update_incident_status(conn, incident_id, "Investigating")
    print(f"Updated {rows_updated} incident(s)")

    # Query
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    # Delete
    rows_deleted = delete_incident(conn, incident_id)
    print(f"Deleted {rows_deleted} incident(s)")


# -----------------------------
# Main
# -----------------------------
def main():
    setup_database_complete()
    conn = connect_database()

    demo_user_auth(conn)
    demo_incidents_crud(conn)

    conn.close()


if __name__ == "__main__":
    main()
