import pandas as pd
import sqlite3

def load_excel_to_sqlite(excel_path: str, table_name: str = "data") -> tuple[sqlite3.Connection, str]:
    """Load Excel/CSV file into SQLite database and return connection and schema"""
    if excel_path.endswith('.csv'):
        df = pd.read_csv(excel_path)
    else:
        df = pd.read_excel(excel_path)
    
    conn = sqlite3.connect(':memory:')
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    schema = f"Table: {table_name}\nColumns:\n"
    for col in columns:
        schema += f"  - {col[1]} ({col[2]})\n"
    
    return conn, schema