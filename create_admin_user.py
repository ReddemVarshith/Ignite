
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs_admin.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'Anime@123'
email = 'admin@example.com'

try:
    if User.objects.filter(username=username).exists():
        print(f"User {username} exists. Updating password.")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
    else:
        print(f"Creating user {username}.")
        User.objects.create_superuser(username, email, password)
    print("Success: Admin user configured.")
except Exception as e:
    print(f"Error: {e}")
