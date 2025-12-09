# app/data/incidents.py

import pandas as pd
from app.data.db import connect_database

# -----------------------------
# CRUD Functions
# -----------------------------

def insert_incident(conn, date, incident_type, severity, status, description, reported_by):
    """Insert a new incident and return its ID"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def get_all_incidents(conn):
    """Return all incidents as a DataFrame"""
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

def update_incident_status(conn, incident_id, new_status):
    """Update the status of an incident and return number of rows updated"""
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """Delete an incident and return number of rows deleted"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount

# -----------------------------
# Analytical Functions
# -----------------------------

def get_incidents_by_type_count(conn):
    """Return a DataFrame counting incidents grouped by incident_type"""
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """Return a DataFrame of high severity incidents grouped by status"""
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    """
    df = pd.read_sql_query(query, conn)
    return df
