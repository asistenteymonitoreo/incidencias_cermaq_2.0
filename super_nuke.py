import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def nuke_all_indices_and_tables():
    with connection.cursor() as cursor:
        print("Borrando TODO el contenido de la base de datos...")
        # Esta es la forma más agresiva de limpiar el esquema público en Postgres
        cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
        cursor.execute("GRANT ALL ON SCHEMA public TO public;")
        print("✅ Base de datos reseteada al 100%.")

if __name__ == "__main__":
    nuke_all_indices_and_tables()
