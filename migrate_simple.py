import os
import django
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Centro, Incidencia

print("🔄 Migración simplificada de datos...\n")

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

def parse_datetime(dt_str):
    if not dt_str:
        return datetime.now()
    try:
        for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return datetime.now()
    except:
        return datetime.now()

# 1. Crear Centro "cipreses" si no existe
print("📊 Creando Centro 'cipreses'...")
centro, created = Centro.objects.get_or_create(
    id='cipreses',
    defaults={'nombre': 'Cipreses', 'slug': 'cipreses'}
)
status = "✓ Creado" if created else "↻ Ya existe"
print(f"  {status}: {centro.nombre}\n")

# 2. Migrar Incidencia
print("📊 Migrando incidencia...")
cursor.execute("SELECT * FROM incidencias_incidencia")
inc_row = cursor.fetchone()

if inc_row:
    inc_dict = dict(inc_row)
    print(f"\nDatos encontrados:")
    for key, value in inc_dict.items():
        if value:
            print(f"  {key}: {value}")
    
    try:
        incidencia, created = Incidencia.objects.update_or_create(
            id=inc_dict['id'],
            defaults={
                'fecha_hora': parse_datetime(inc_dict.get('fecha_hora')),
                'turno': inc_dict.get('turno', 'dia'),
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
                'riesgo_peces': bool(inc_dict.get('riesgo_peces', 0)),
                'perdida_economica': bool(inc_dict.get('perdida_economica', 0)),
                'riesgo_personas': bool(inc_dict.get('riesgo_personas', 0)),
                'observacion': inc_dict.get('observacion', ''),
                'tipo_incidencia_normalizada': inc_dict.get('tipo_incidencia_normalizada', ''),
            }
        )
        status = "✓ Creada" if created else "↻ Actualizada"
        print(f"\n{status}: Incidencia #{incidencia.id}")
        print(f"  Centro: {incidencia.centro.nombre}")
        print(f"  Fecha: {incidencia.fecha_hora}")
        print(f"  Tipo: {incidencia.tipo_incidencia}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("  No se encontraron incidencias")

sqlite_conn.close()

print("\n" + "="*60)
print("✅ MIGRACIÓN COMPLETADA")
print("="*60)
