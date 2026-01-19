-- Script para LIMPIAR COMPLETAMENTE la base de datos en Supabase
-- Ejecuta este script PRIMERO en el Editor SQL de Supabase

-- Eliminar todas las tablas de Django si existen
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;

-- Eliminar tablas de la aplicación incidencias si existen
DROP TABLE IF EXISTS incidencias_centro CASCADE;
DROP TABLE IF EXISTS incidencias_operario CASCADE;
DROP TABLE IF EXISTS incidencias_incidencia CASCADE;
DROP TABLE IF EXISTS incidencias_controldiario CASCADE;
DROP TABLE IF EXISTS incidencias_reportecamaras CASCADE;

-- Limpiar secuencias si existen
DROP SEQUENCE IF EXISTS django_migrations_id_seq CASCADE;
DROP SEQUENCE IF EXISTS django_content_type_id_seq CASCADE;
DROP SEQUENCE IF EXISTS auth_permission_id_seq CASCADE;
DROP SEQUENCE IF EXISTS auth_group_id_seq CASCADE;
DROP SEQUENCE IF EXISTS auth_user_id_seq CASCADE;
DROP SEQUENCE IF EXISTS django_admin_log_id_seq CASCADE;
DROP SEQUENCE IF EXISTS incidencias_incidencia_id_seq CASCADE;
DROP SEQUENCE IF EXISTS incidencias_controldiario_id_seq CASCADE;
DROP SEQUENCE IF EXISTS incidencias_reportecamaras_id_seq CASCADE;

-- Mensaje de confirmación
SELECT 'Base de datos limpiada completamente. Ahora ejecuta: python manage.py migrate' AS status;
