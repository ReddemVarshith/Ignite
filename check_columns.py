
import os
import django
from django.conf import settings
import psycopg2
from dotenv import load_dotenv

load_dotenv()
dsn = os.getenv('DATABASE_URL')

def get_columns(table_name):
    try:
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """)
        cols = cur.fetchall()
        conn.close()
        return cols
    except Exception as e:
        print(f"Error {table_name}: {e}")
        return []

tables = ['web_registration', 'web_teammember', 'events_registration', 'events_teammember']
for t in tables:
    print(f"\nTABLE: {t}")
    cols = get_columns(t)
    for c in cols:
        print(f"  {c[0]} ({c[1]}) check_null={c[2]}")
