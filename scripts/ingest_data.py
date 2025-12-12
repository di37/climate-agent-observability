#!/usr/bin/env python3
"""
Script to ingest climate change CSV data into SQLite database.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Define file paths
CSV_FILE = Path(__file__).parent / "data" / "climate_change_impact_on_agriculture_2024.csv"
DB_FILE = Path(__file__).parent / "data" / "climate_agriculture.db"

def ingest_csv_to_sqlite():
    """
    Read CSV file and ingest into SQLite database.
    Creates a table called 'climate_agriculture_data' with all columns from the CSV.
    """
    print(f"Reading CSV file: {CSV_FILE}")
    
    # Read CSV file
    df = pd.read_csv(CSV_FILE)
    
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # Create SQLite database connection
    print(f"\nCreating SQLite database: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    
    # Ingest data into SQLite
    # if_exists='replace' will drop and recreate the table if it exists
    table_name = "climate_agriculture_data"
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    print(f"\n✓ Successfully ingested {len(df)} rows into table '{table_name}'")
    
    # Verify the data
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    print(f"✓ Verified: Database contains {row_count} rows")
    
    # Show table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    print(f"\nTable Schema:")
    for col in schema:
        print(f"  - {col[1]} ({col[2]})")
    
    # Show sample query
    print(f"\nSample query result (first 3 rows):")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  {row[:5]}...")  # Show first 5 columns
    
    # Close connection
    conn.close()
    print(f"\n✓ Database created successfully at: {DB_FILE}")

if __name__ == "__main__":
    ingest_csv_to_sqlite()

