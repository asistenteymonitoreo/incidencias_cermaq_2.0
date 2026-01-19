-- Script DEFINITIVO para limpiar COMPLETAMENTE Supabase
-- Este script elimina TODO el esquema público y lo recrea desde cero

-- 1. Eliminar el esquema público completo (esto elimina TODAS las tablas)
DROP SCHEMA IF EXISTS public CASCADE;

-- 2. Recrear el esquema público vacío
CREATE SCHEMA public;

-- 3. Dar permisos necesarios
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Mensaje de confirmación
SELECT 'Base de datos completamente limpia. Ejecuta ahora: python manage.py migrate' AS status;
