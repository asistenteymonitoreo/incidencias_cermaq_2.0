import os
import django
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from incidencias.models import Centro, Incidencia

print("🔄 Migración de datos (versión robusta)...\n")

# Conectar a SQLite
try:
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
    
    # 1. Crear Centro "cipreses"
    print("📊 Creando Centro 'cipreses'...")
    try:
        centro, created = Centro.objects.get_or_create(
            id='cipreses',
            defaults={'nombre': 'Cipreses', 'slug': 'cipreses'}
        )
        status = "✓ Creado" if created else "↻ Ya existe"
        print(f"  {status}: {centro.nombre}\n")
    except Exception as e:
        print(f"  ✗ Error creando centro: {e}\n")
        centro = None
    
    # 2. Leer incidencia de SQLite
    print("📊 Leyendo incidencia de SQLite...")
    cursor.execute("SELECT * FROM incidencias_incidencia LIMIT 1")
    inc_row = cursor.fetchone()
    
    if not inc_row:
        print("  No se encontraron incidencias en SQLite")
    elif not centro:
        print("  No se pudo crear el centro, abortando migración")
    else:
        inc_dict = dict(inc_row)
        print(f"  Encontrada incidencia ID: {inc_dict.get('id')}\n")
        
        # 3. Crear incidencia en Supabase
        print("📊 Creando incidencia en Supabase...")
        try:
            incidencia = Incidencia(
                fecha_hora=parse_datetime(inc_dict.get('fecha_hora')),
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
            print(f"    ID: {incidencia.id}")
            print(f"    Centro: {incidencia.centro.nombre}")
            print(f"    Fecha: {incidencia.fecha_hora}")
            print(f"    Tipo: {incidencia.tipo_incidencia}")
            
        except Exception as e:
            print(f"  ✗ Error creando incidencia: {e}")
            import traceback
            traceback.print_exc()
    
    sqlite_conn.close()
    
except Exception as e:
    print(f"✗ Error general: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✅ PROCESO COMPLETADO")
print("="*60)
