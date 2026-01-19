import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]
    return tables

if __name__ == "__main__":
    tables = list_tables()
    print("Tablas encontradas en Supabase:")
    for table in sorted(tables):
        print(f"- {table}")
    
    if not tables:
        print("No se encontraron tablas.")
