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

from incidencias.models import Centro, Operario, Incidencia
from django.db import transaction

print("🔄 Iniciando migración completa de datos...\n")

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# Función auxiliar para convertir fechas
def parse_datetime(dt_str):
    if not dt_str:
        return datetime.now()
    try:
        for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return datetime.now()
    except:
        return datetime.now()

# 1. Migrar Centros
print("📊 Migrando Centros...")
cursor.execute("SELECT * FROM incidencias_centro")
centros_sqlite = cursor.fetchall()
centro_map = {}

for centro_row in centros_sqlite:
    try:
        centro_dict = dict(centro_row)
        centro, created = Centro.objects.update_or_create(
            id=centro_dict['id'],
            defaults={
                'nombre': centro_dict['nombre'],
                'slug': centro_dict.get('slug', centro_dict['id']),
            }
        )
        centro_map[centro_dict['id']] = centro
        status = "✓ Creado" if created else "↻ Actualizado"
        print(f"  {status}: {centro.nombre}")
    except Exception as e:
        print(f"  ✗ Error con centro {centro_dict.get('id', '?')}: {e}")

print(f"\n✅ Centros migrados: {len(centro_map)}\n")

# 2. Migrar Operarios
print("📊 Migrando Operarios...")
cursor.execute("SELECT * FROM incidencias_operario")
operarios_sqlite = cursor.fetchall()
operario_map = {}

for op_row in operarios_sqlite:
    try:
        op_dict = dict(op_row)
        centro = centro_map.get(op_dict['centro_id'])
        
        if not centro:
            print(f"  ⚠️  Centro {op_dict['centro_id']} no encontrado para operario {op_dict['id']}")
            continue
            
        operario, created = Operario.objects.update_or_create(
            id=op_dict['id'],
            defaults={
                'nombre': op_dict['nombre'],
                'cargo': op_dict.get('cargo', ''),
                'telefono': op_dict.get('telefono', ''),
                'centro': centro,
            }
        )
        operario_map[op_dict['id']] = operario
        status = "✓ Creado" if created else "↻ Actualizado"
        print(f"  {status}: {operario.nombre}")
    except Exception as e:
        print(f"  ✗ Error con operario {op_dict.get('id', '?')}: {e}")

print(f"\n✅ Operarios migrados: {len(operario_map)}\n")

# 3. Migrar Incidencias
print("📊 Migrando Incidencias...")
cursor.execute("SELECT * FROM incidencias_incidencia")
incidencias_sqlite = cursor.fetchall()

incidencia_count = 0
for inc_row in incidencias_sqlite:
    try:
        inc_dict = dict(inc_row)
        
        # Obtener el centro
        centro = centro_map.get(inc_dict.get('centro_id'))
        
        # Obtener el operario de contacto
        operario_contacto = None
        if inc_dict.get('operario_contacto_id'):
            operario_contacto = operario_map.get(inc_dict['operario_contacto_id'])
        
        # Crear o actualizar la incidencia
        incidencia, created = Incidencia.objects.update_or_create(
            id=inc_dict['id'],
            defaults={
                'fecha_hora': parse_datetime(inc_dict.get('fecha_hora')),
                'turno': inc_dict.get('turno', ''),
                'centro': centro,
                'tipo_incidencia': inc_dict.get('tipo_incidencia', ''),
                'modulo': inc_dict.get('modulo', ''),
                'estanque': inc_dict.get('estanque', ''),
                'parametros_afectados': inc_dict.get('parametros_afectados', ''),
                'oxigeno_nivel': inc_dict.get('oxigeno_nivel', ''),
                'oxigeno_valor': inc_dict.get('oxigeno_valor', ''),
                'temperatura_nivel': inc_dict.get('temperatura_nivel', ''),
                'temperatura_valor': inc_dict.get('temperatura_valor', ''),
                'conductividad_nivel': inc_dict.get('conductividad_nivel', ''),
                'turbidez_nivel': inc_dict.get('turbidez_nivel', ''),
                'turbidez_valor': inc_dict.get('turbidez_valor', ''),
                'sistema_sensor': inc_dict.get('sistema_sensor', ''),
                'sensor_detectado': inc_dict.get('sensor_detectado', ''),
                'sensor_nivel': inc_dict.get('sensor_nivel', ''),
                'sensor_valor': inc_dict.get('sensor_valor', ''),
                'tiempo_resolucion': inc_dict.get('tiempo_resolucion'),
                'riesgo_peces': bool(inc_dict.get('riesgo_peces', False)),
                'perdida_economica': bool(inc_dict.get('perdida_economica', False)),
                'riesgo_personas': bool(inc_dict.get('riesgo_personas', False)),
                'observacion': inc_dict.get('observacion', ''),
                'operario_contacto': operario_contacto,
                'tipo_incidencia_normalizada': inc_dict.get('tipo_incidencia_normalizada', ''),
            }
        )
        incidencia_count += 1
        status = "✓ Creada" if created else "↻ Actualizada"
        centro_nombre = centro.nombre if centro else "Sin centro"
        print(f"  {status}: Incidencia #{incidencia.id} - {centro_nombre} - {incidencia.turno}")
        
    except Exception as e:
        print(f"  ✗ Error con incidencia {inc_dict.get('id', '?')}: {e}")
        import traceback
        traceback.print_exc()

sqlite_conn.close()

print("\n" + "="*60)
print("✅ MIGRACIÓN COMPLETADA")
print("="*60)
print(f"Centros: {len(centro_map)}")
print(f"Operarios: {len(operario_map)}")
print(f"Incidencias: {incidencia_count}")
print("="*60)
