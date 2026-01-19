import os
import django
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from incidencias.models import *
from django.db import transaction

print("🔄 Iniciando migración completa de datos...\n")

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# Función auxiliar para convertir fechas
def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        # Intentar varios formatos
        for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return None
    except:
        return None

# 1. Migrar Usuarios
print("📊 Migrando usuarios...")
cursor.execute("SELECT * FROM auth_user")
users = cursor.fetchall()
user_map = {}

for user_row in users:
    try:
        user, created = User.objects.update_or_create(
            username=user_row['username'],
            defaults={
                'email': user_row['email'] or '',
                'first_name': user_row['first_name'] or '',
                'last_name': user_row['last_name'] or '',
                'is_staff': bool(user_row['is_staff']),
                'is_active': bool(user_row['is_active']),
                'is_superuser': bool(user_row['is_superuser']),
                'password': user_row['password'],
                'date_joined': parse_datetime(user_row['date_joined']) or datetime.now(),
            }
        )
        user_map[user_row['id']] = user
        status = "✓ Creado" if created else "↻ Actualizado"
        print(f"  {status}: {user.username}")
    except Exception as e:
        print(f"  ✗ Error con usuario {user_row['username']}: {e}")

print(f"\n✅ Usuarios migrados: {len(user_map)}\n")

# 2. Migrar Incidencias
print("📊 Migrando incidencias...")
cursor.execute("SELECT * FROM incidencias_incidencia")
incidencias = cursor.fetchall()

incidencia_count = 0
for inc_row in incidencias:
    try:
        with transaction.atomic():
            # Obtener el usuario si existe
            operario = None
            if inc_row['operario_id']:
                operario = user_map.get(inc_row['operario_id'])
            
            incidencia, created = Incidencia.objects.update_or_create(
                id=inc_row['id'],
                defaults={
                    'fecha': parse_datetime(inc_row['fecha']) or datetime.now(),
                    'piscicultura': inc_row['piscicultura'] or '',
                    'estanque': inc_row['estanque'] or '',
                    'tipo_incidencia': inc_row['tipo_incidencia'] or '',
                    'descripcion': inc_row['descripcion'] or '',
                    'operario': operario,
                    'estado': inc_row['estado'] or 'pendiente',
                }
            )
            incidencia_count += 1
            status = "✓" if created else "↻"
            print(f"  {status} Incidencia #{incidencia.id} - {incidencia.piscicultura}")
    except Exception as e:
        print(f"  ✗ Error con incidencia {inc_row['id']}: {e}")

print(f"\n✅ Incidencias migradas: {incidencia_count}\n")

# 3. Migrar otras tablas si existen
tables_to_check = [
    'incidencias_reportecamaras',
    'incidencias_controldiario',
    'incidencias_novedades',
]

for table_name in tables_to_check:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"📊 Encontrados {count} registros en {table_name}")
            print(f"  ⚠️  Migración manual requerida para esta tabla\n")
    except sqlite3.OperationalError:
        # Tabla no existe
        pass

sqlite_conn.close()

print("\n" + "="*50)
print("✅ MIGRACIÓN COMPLETADA")
print("="*50)
print(f"Usuarios: {len(user_map)}")
print(f"Incidencias: {incidencia_count}")
