-- Script para eliminar índices problemáticos específicos
-- Ejecuta esto en Supabase ANTES de las migraciones

-- Eliminar índices específicos que están causando problemas
DROP INDEX IF EXISTS incidencias_incidencia_0e0c0c87_like CASCADE;
DROP INDEX IF EXISTS incidencias_incidencia_c29ff9a7_like CASCADE;

-- Eliminar todas las tablas de incidencias si existen
DROP TABLE IF EXISTS incidencias_incidencia CASCADE;
DROP TABLE IF EXISTS incidencias_centro CASCADE;
DROP TABLE IF EXISTS incidencias_operario CASCADE;
DROP TABLE IF EXISTS incidencias_controldiario CASCADE;
DROP TABLE IF EXISTS incidencias_reportecamaras CASCADE;

-- Eliminar tablas de Django
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

SELECT 'Limpieza completa. Ahora ejecuta: python manage.py migrate' AS status;
