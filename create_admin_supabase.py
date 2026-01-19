"""
Script para crear usuario admin en Supabase
Ejecuta este script después de cambiar settings.py a Supabase
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@cermaq.com',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True,
        'first_name': 'Admin',
        'last_name': 'Cermaq'
    }
)

if created:
    user.set_password('admin123')
    user.save()
    print('✅ Usuario admin creado exitosamente')
else:
    user.set_password('admin123')
    user.save()
    print('✅ Contraseña de admin actualizada')

print('\n📋 Credenciales:')
print('Usuario: admin')
print('Contraseña: admin123')
print('\n⚠️  IMPORTANTE: Cambia esta contraseña después del primer login')
