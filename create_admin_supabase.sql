-- Script SQL para crear usuario admin en Supabase
-- Ejecuta este script en el Editor SQL de Supabase

-- 1. Crear el usuario admin
INSERT INTO auth_user (
    id,
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    1,
    'pbkdf2_sha256$600000$YourRandomSalt123456$HashPasswordHere',  -- Esta es una contraseña temporal
    NULL,
    true,
    'admin',
    'Admin',
    'User',
    'admin@cermaq.com',
    true,
    true,
    NOW()
);

-- IMPORTANTE: Después de ejecutar este script, debes cambiar la contraseña
-- usando el comando de Django:
-- python manage.py changepassword admin

-- O mejor aún, usa este script Python para crear el usuario correctamente:
