
import os
import django
from django.conf import settings
import psycopg2
from urllib.parse import urlparse

# Setup Django (optional, but good for context)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs_admin.settings')
django.setup()

db_url = settings.DATABASES['default']['NAME']
# DJ-database-url config puts the URL in 'NAME' if using sqlite, but for postgres it's different.
# Let's just use the env var directly as it's safer.
from dotenv import load_dotenv
load_dotenv()
dsn = os.getenv('DATABASE_URL')

print(f"Connecting to DB...")
try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    
    # List all tables in public schema
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
        
    print("\n--- Checking specifically for codestorm_registrations ---")
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name = 'codestorm_registrations';")
    match = cur.fetchone()
    if match:
        print(f"FOUND: {match}")
    else:
        print("NOT FOUND in information_schema.tables")

    conn.close()
except Exception as e:
    print(f"Error: {e}")
