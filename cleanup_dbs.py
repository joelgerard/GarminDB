
import sqlite3
import os
import datetime

db_dir = os.path.expanduser('~/HealthData/DBs')
target_date = '2026-01-05'

dbs = [
    'garmin.db',
    'garmin_monitoring.db',
    'garmin_activities.db',
    'garmin_summary.db',
    'summary.db'
]

def clean_db(db_name):
    db_path = os.path.join(db_dir, db_name)
    if not os.path.exists(db_path):
        print(f"Skipping {db_name}, not found.")
        return

    print(f"Cleaning {db_name}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        # Check if table has 'day', 'timestamp', or 'start_time' column
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
        
        delete_sql = None
        if 'day' in columns:
            delete_sql = f"DELETE FROM {table} WHERE day >= ?"
        elif 'timestamp' in columns:
            delete_sql = f"DELETE FROM {table} WHERE timestamp >= ?"
        elif 'start_time' in columns:
            delete_sql = f"DELETE FROM {table} WHERE start_time >= ?"
        
        if delete_sql:
            print(f"  Deleting from {table}...")
            cursor.execute(delete_sql, (target_date,))
            print(f"    Rows deleted: {conn.total_changes}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    for db in dbs:
        clean_db(db)
