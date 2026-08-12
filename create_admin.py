import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user, created = User.objects.get_or_create(
    username='admin', 
    defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
)

user.set_password('admin1234')
user.is_staff = True
user.is_superuser = True
user.save()

print("Contraseña de 'admin' actualizada exitosamente a 'admin1234'.")