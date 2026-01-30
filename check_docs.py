
import os
import sys
import django

# Add project root to Python path
sys.path.append('c:/Users/sanja/OneDrive/Desktop/ignite_admin')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ignite_admin.settings')
django.setup()

from website_fixed.models import WebRegistration

regs = WebRegistration.objects.all()
print(f"Total entries: {regs.count()}")

for reg in regs:
    print(f"ID: {reg.id}, Document: '{reg.project_document}'")
