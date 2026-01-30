
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ignite_admin.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'web_registration'")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in web_registration:")
    for col in columns:
        print(f"- {col}")
