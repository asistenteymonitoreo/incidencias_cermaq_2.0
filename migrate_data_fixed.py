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
from incidencias.models import Incidencia
from django.db import transaction

print("🔄 Iniciando migración de datos...\n")

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# Función auxiliar para convertir fechas
def parse_datetime(dt_str):
    if not dt_str:
        return datetime.now()
    try:
        # Intentar varios formatos
        for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return datetime.now()
    except:
        return datetime.now()

# Primero, ver qué hay en la tabla
print("📊 Verificando datos en SQLite...")
cursor.execute("SELECT * FROM incidencias_incidencia")
incidencias_sqlite = cursor.fetchall()
print(f"Encontradas {len(incidencias_sqlite)} incidencias en SQLite\n")

if len(incidencias_sqlite) > 0:
    print("Estructura de la primera incidencia:")
    first = dict(incidencias_sqlite[0])
    for key, value in first.items():
        print(f"  {key}: {value}")
    print()

# Migrar Incidencias
print("📊 Migrando incidencias a Supabase...")
incidencia_count = 0
error_count = 0

for inc_row in incidencias_sqlite:
    try:
        # Convertir a diccionario para facilitar acceso
        inc_dict = dict(inc_row)
        
        # Obtener el usuario si existe
        operario = None
        if inc_dict.get('operario_id'):
            try:
                operario = User.objects.get(id=inc_dict['operario_id'])
            except User.DoesNotExist:
                print(f"  ⚠️  Usuario {inc_dict['operario_id']} no existe, creando incidencia sin operario")
        
        # Crear o actualizar la incidencia
        incidencia, created = Incidencia.objects.update_or_create(
            id=inc_dict['id'],
            defaults={
                'fecha': parse_datetime(inc_dict.get('fecha')),
                'piscicultura': inc_dict.get('piscicultura', ''),
                'estanque': inc_dict.get('estanque', ''),
                'tipo_incidencia': inc_dict.get('tipo_incidencia', ''),
                'descripcion': inc_dict.get('descripcion', ''),
                'operario': operario,
                'estado': inc_dict.get('estado', 'pendiente'),
            }
        )
        incidencia_count += 1
        status = "✓ Creada" if created else "↻ Actualizada"
        print(f"  {status}: Incidencia #{incidencia.id} - {incidencia.piscicultura} - {incidencia.tipo_incidencia}")
        
    except Exception as e:
        error_count += 1
        print(f"  ✗ Error con incidencia {inc_dict.get('id', '?')}: {e}")
        import traceback
        traceback.print_exc()

sqlite_conn.close()

print("\n" + "="*60)
print("✅ MIGRACIÓN COMPLETADA")
print("="*60)
print(f"Incidencias migradas exitosamente: {incidencia_count}")
print(f"Errores: {error_count}")
print("="*60)
