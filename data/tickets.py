# app/data/tickets.py
import pandas as pd

def insert_ticket(conn, ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    conn.commit()
    return cursor.lastrowid

def get_all_tickets(conn):
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    return df

def update_ticket_status(conn, ticket_id, new_status):
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount
