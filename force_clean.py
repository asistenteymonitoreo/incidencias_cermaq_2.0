import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def force_delete_everything():
    tables = [
        'incidencias_incidencia', 'incidencias_centro', 'incidencias_operario',
        'incidencias_controldiario', 'incidencias_reportecamaras',
        'django_migrations', 'django_session', 'django_admin_log',
        'auth_user_user_permissions', 'auth_user_groups', 'auth_permission',
        'auth_user', 'auth_group_permissions', 'auth_group', 'django_content_type'
    ]
    
    with connection.cursor() as cursor:
        print("Eliminando tablas e índices uno por uno...")
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                print(f"- Tabla {table} eliminada.")
            except Exception as e:
                print(f"- Error eliminando {table}: {e}")
        
        # Eliminar índices problemáticos conocidos
        indices = ['incidencias_incidencia_c29ff9a7_like', 'incidencias_incidencia_0e0c0c87_like']
        for idx in indices:
            try:
                cursor.execute(f"DROP INDEX IF EXISTS {idx} CASCADE;")
                print(f"- Índice {idx} eliminado.")
            except Exception as e:
                print(f"- Error eliminando índice {idx}: {e}")
                
if __name__ == "__main__":
    force_delete_everything()
