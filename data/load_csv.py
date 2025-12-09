import pandas as pd
from pathlib import Path

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    csv_path = Path(csv_path)

    # Check if CSV file exists
    if not csv_path.exists():
        print(f" CSV file not found: {csv_path}")
        return 0

    try:
        # Read CSV into pandas DataFrame
        df = pd.read_csv(csv_path)

        # Insert data into database
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',  # add to existing table
            index=False          # do not include DataFrame index as column
        )

        print(f"Loaded {len(df)} rows from {csv_path.name} into '{table_name}' table.")
        return len(df)

    except Exception as e:
        print(f" Failed to load {csv_path.name} into '{table_name}': {e}")
        return 0
