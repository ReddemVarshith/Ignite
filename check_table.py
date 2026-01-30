
import os
import django
from django.conf import settings
import psycopg2
from dotenv import load_dotenv

load_dotenv()
dsn = os.getenv('DATABASE_URL')

def check_table_content(dsn_string, table_name):
    print(f"\nChecking table: {table_name}")
    try:
        conn = psycopg2.connect(dsn_string)
        cur = conn.cursor()
        
        # Get row count
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cur.fetchone()[0]
        print(f"Row count: {count}")
        
        # Get columns
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}';
        """)
        cols = cur.fetchall()
        print(f"Columns: {[c[0] for c in cols]}")
        
        # Sample data
        if count > 0:
            cur.execute(f"SELECT * FROM {table_name} LIMIT 1;")
            row = cur.fetchone()
            print(f"Sample row: {row}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

check_table_content(dsn, 'web_registration')
check_table_content(dsn, 'events_registration')
