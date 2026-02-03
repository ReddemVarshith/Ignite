from website_fixed.models import WebRegistration
from django.db import connection

# Get all columns from the web_registration table
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'web_registration'
        ORDER BY ordinal_position
    """)
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in web_registration table:")
    for col in columns:
        print(f"  - {col}")
    
    # Check if project_category exists
    if 'project_category' in columns:
        print("\n✓ project_category column EXISTS in database")
    else:
        print("\n✗ project_category column DOES NOT exist in database")
