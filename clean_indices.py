import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def nuke_problematic_index():
    with connection.cursor() as cursor:
        print("Borrando índices y tablas problemáticas específicamente...")
        try:
            cursor.execute("DROP INDEX IF EXISTS incidencias_incidencia_c29ff9a7_like CASCADE;")
            cursor.execute("DROP INDEX IF EXISTS incidencias_incidencia_0e0c0c87_like CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS incidencias_incidencia CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS django_migrations CASCADE;")
            print("✅ Limpieza específica completada.")
        except Exception as e:
            print(f"Error durante la limpieza: {e}")

if __name__ == "__main__":
    nuke_problematic_index()
