
import os
import django
from django.conf import settings
import psycopg2
from dotenv import load_dotenv

load_dotenv()
dsn = os.getenv('DATABASE_URL')

def inspect_db(dsn_string):
    print(f"Connecting to: {dsn_string.split('@')[-1]}")
    try:
        conn = psycopg2.connect(dsn_string)
        cur = conn.cursor()
        
        # List all schemas
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cur.fetchall()
        print(f"Schemas: {[s[0] for s in schemas]}")

        # List all tables in all schemas
        cur.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name;
        """)
        tables = cur.fetchall()
        print("\n--- All Tables ---")
        for schema, table in tables:
            print(f"{schema}.{table}")

        # Check columns of relevant tables
        target_tables = ['web_registration', 'events_registration', 'codestorm_registrations']
        for t in target_tables:
            print(f"\nScanning table: {t}...")
            # We don't know the schema, so we search
            cur.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{t}';
            """)
            cols = cur.fetchall()
            if cols:
                print(f"Found {t} columns: {[c[0] for c in cols]}")
            else:
                print(f"Table {t} NOT FOUND in any schema (or no columns).")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

print("Checking 'neondb' database...")
inspect_db(dsn)

# Try 'postgres' database if possible
if 'neondb' in dsn:
    dsn_postgres = dsn.replace('/neondb', '/postgres')
    print("\nChecking 'postgres' database...")
    inspect_db(dsn_postgres)
