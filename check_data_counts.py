
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs_admin.settings')
django.setup()

from website_fixed.models import WebRegistration
from dashboard.models import EventsRegistration

try:
    web_count = WebRegistration.objects.count()
    events_count = EventsRegistration.objects.count()
    
    print(f"WebRegistration count: {web_count}")
    print(f"EventsRegistration count: {events_count}")
    
    if web_count > 0:
        print("Sample WebRegistration:", WebRegistration.objects.first().__dict__)
    if events_count > 0:
        print("Sample EventsRegistration:", EventsRegistration.objects.first().__dict__)

except Exception as e:
    print(f"Error: {e}")
