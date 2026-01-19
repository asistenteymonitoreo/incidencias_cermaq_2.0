import os
import django
import sqlite3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from incidencias.models import *

print("🔄 Iniciando migración de datos...")

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# Migrar usuarios
print("\n📊 Migrando usuarios...")
cursor.execute("SELECT * FROM auth_user")
users = cursor.fetchall()
user_map = {}

for user_row in users:
    try:
        user, created = User.objects.update_or_create(
            username=user_row['username'],
            defaults={
                'email': user_row['email'],
                'first_name': user_row['first_name'],
                'last_name': user_row['last_name'],
                'is_staff': user_row['is_staff'],
                'is_active': user_row['is_active'],
                'is_superuser': user_row['is_superuser'],
                'password': user_row['password'],
                'date_joined': user_row['date_joined'],
            }
        )
        user_map[user_row['id']] = user
        print(f"  ✓ Usuario: {user.username}")
    except Exception as e:
        print(f"  ✗ Error con usuario {user_row['username']}: {e}")

# Obtener todos los modelos de incidencias
print("\n📊 Obteniendo modelos de incidencias...")

# Listar todas las tablas de incidencias
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'incidencias_%'")
tables = cursor.fetchall()

for table in tables:
    table_name = table['name']
    print(f"\n📋 Procesando tabla: {table_name}")
    
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"  Encontrados {len(rows)} registros")
        
        # Aquí puedes agregar lógica específica para cada modelo
        # Por ahora solo mostramos el conteo
        
    except Exception as e:
        print(f"  ✗ Error procesando {table_name}: {e}")

print("\n✅ Migración completada!")
sqlite_conn.close()
