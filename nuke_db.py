import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def nuke_public_schema():
    with connection.cursor() as cursor:
        print("Limpiando esquema público...")
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
        cursor.execute("GRANT ALL ON SCHEMA public TO public;")
        print("✅ Esquema público limpio y recreado.")

if __name__ == "__main__":
    nuke_public_schema()
