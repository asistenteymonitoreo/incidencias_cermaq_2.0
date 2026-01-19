import os
import sys
import django
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Centro, Incidencia

print("="*60)
print("MIGRACIÓN DE DATOS - SQLite a Supabase PostgreSQL")
print("="*60)

# Paso 1: Verificar SQLite
print("\n[1/4] Verificando datos en SQLite...")
try:
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM incidencias_incidencia")
    count = cursor.fetchone()[0]
    print(f"  ✓ Encontradas {count} incidencias en SQLite")
    
    if count == 0:
        print("  ⚠️  No hay datos para migrar")
        sys.exit(0)
        
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Paso 2: Crear Centro
print("\n[2/4] Creando Centro 'Cipreses' en Supabase...")
try:
    centro, created = Centro.objects.get_or_create(
        id='cipreses',
        defaults={'nombre': 'Cipreses', 'slug': 'cipreses'}
    )
    if created:
        print(f"  ✓ Centro creado: {centro.nombre}")
    else:
        print(f"  ↻ Centro ya existe: {centro.nombre}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Paso 3: Leer incidencia de SQLite
print("\n[3/4] Leyendo incidencia de SQLite...")
try:
    cursor.execute("SELECT * FROM incidencias_incidencia LIMIT 1")
    inc_row = cursor.fetchone()
    
    if not inc_row:
        print("  ⚠️  No se encontró ninguna incidencia")
        sys.exit(0)
    
    inc_dict = dict(inc_row)
    print(f"  ✓ Incidencia encontrada (ID: {inc_dict.get('id')})")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Paso 4: Crear incidencia en Supabase
print("\n[4/4] Creando incidencia en Supabase...")
try:
    def parse_dt(dt_str):
        if not dt_str:
            return datetime.now()
        for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S']:
            try:
                return datetime.strptime(dt_str, fmt)
            except:
                continue
        return datetime.now()
    
    incidencia = Incidencia(
        fecha_hora=parse_dt(inc_dict.get('fecha_hora')),
        turno=inc_dict.get('turno') or 'dia',
        centro=centro,
        tipo_incidencia=inc_dict.get('tipo_incidencia') or '',
        modulo=inc_dict.get('modulo') or '',
        estanque=inc_dict.get('estanque') or '',
        parametros_afectados=inc_dict.get('parametros_afectados') or '',
        oxigeno_nivel=inc_dict.get('oxigeno_nivel') or '',
        oxigeno_valor=inc_dict.get('oxigeno_valor') or '',
        temperatura_nivel=inc_dict.get('temperatura_nivel') or '',
        temperatura_valor=inc_dict.get('temperatura_valor') or '',
        conductividad_nivel=inc_dict.get('conductividad_nivel') or '',
        turbidez_nivel=inc_dict.get('turbidez_nivel') or '',
        turbidez_valor=inc_dict.get('turbidez_valor') or '',
        sistema_sensor=inc_dict.get('sistema_sensor') or '',
        sensor_detectado=inc_dict.get('sensor_detectado') or '',
        sensor_nivel=inc_dict.get('sensor_nivel') or '',
        sensor_valor=inc_dict.get('sensor_valor') or '',
        tiempo_resolucion=inc_dict.get('tiempo_resolucion'),
        riesgo_peces=bool(inc_dict.get('riesgo_peces', 0)),
        perdida_economica=bool(inc_dict.get('perdida_economica', 0)),
        riesgo_personas=bool(inc_dict.get('riesgo_personas', 0)),
        observacion=inc_dict.get('observacion') or '',
        tipo_incidencia_normalizada=inc_dict.get('tipo_incidencia_normalizada') or '',
    )
    incidencia.save()
    
    print(f"  ✓ Incidencia creada exitosamente!")
    print(f"    - ID: {incidencia.id}")
    print(f"    - Centro: {incidencia.centro.nombre}")
    print(f"    - Fecha: {incidencia.fecha_hora}")
    print(f"    - Tipo: {incidencia.tipo_incidencia or 'N/A'}")
    print(f"    - Turno: {incidencia.turno}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

sqlite_conn.close()

print("\n" + "="*60)
print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
print("="*60)
print(f"\nResumen:")
print(f"  - 1 Centro creado/verificado")
print(f"  - 1 Incidencia migrada")
print(f"\nLa base de datos en Supabase está lista para usar!")
