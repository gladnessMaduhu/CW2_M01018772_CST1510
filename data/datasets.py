# app/data/datasets.py
import pandas as pd

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    return df

def update_dataset(conn, dataset_id, **kwargs):
    columns = ', '.join([f"{k} = ?" for k in kwargs])
    values = list(kwargs.values())
    values.append(dataset_id)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE datasets_metadata SET {columns} WHERE id = ?", values)
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount
