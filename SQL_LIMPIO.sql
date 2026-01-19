-- LIMPIEZA TOTAL
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- TABLAS DJANGO
CREATE TABLE "django_content_type" (
    "id" serial PRIMARY KEY,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);

CREATE TABLE "auth_permission" (
    "id" serial PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);

CREATE TABLE "auth_group" (
    "id" serial PRIMARY KEY,
    "name" varchar(150) NOT NULL UNIQUE
);

CREATE TABLE "auth_group_permissions" (
    "id" serial PRIMARY KEY,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id")
);

CREATE TABLE "auth_user" (
    "id" serial PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" timestamptz,
    "is_superuser" boolean NOT NULL,
    "username" varchar(150) NOT NULL UNIQUE,
    "first_name" varchar(150) NOT NULL,
    "last_name" varchar(150) NOT NULL,
    "email" varchar(254) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "date_joined" timestamptz NOT NULL
);

CREATE TABLE "auth_user_groups" (
    "id" serial PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
);

CREATE TABLE "auth_user_user_permissions" (
    "id" serial PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
);

CREATE TABLE "django_session" (
    "session_key" varchar(40) PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamptz NOT NULL
);
CREATE INDEX "django_session_expire_date" ON "django_session" ("expire_date");

-- TABLAS INCIDENCIAS
CREATE TABLE "incidencias_centro" (
    "id" varchar(50) PRIMARY KEY,
    "nombre" varchar(100) NOT NULL UNIQUE,
    "slug" varchar(100) NOT NULL UNIQUE
);

CREATE TABLE "incidencias_operario" (
    "id" integer PRIMARY KEY,
    "nombre" varchar(200) NOT NULL,
    "cargo" varchar(200) NOT NULL,
    "telefono" varchar(50) NOT NULL,
    "centro_id" varchar(50) NOT NULL REFERENCES "incidencias_centro" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE "incidencias_incidencia" (
    "id" serial PRIMARY KEY,
    "fecha_hora" timestamptz NOT NULL,
    "turno" varchar(50) NOT NULL,
    "centro_id" varchar(50) REFERENCES "incidencias_centro" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_incidencia" varchar(50) NOT NULL,
    "modulo" varchar(100) NOT NULL,
    "estanque" varchar(100) NOT NULL,
    "parametros_afectados" varchar(500) NOT NULL,
    "oxigeno_nivel" varchar(50) NOT NULL,
    "oxigeno_valor" varchar(50) NOT NULL,
    "temperatura_nivel" varchar(50) NOT NULL,
    "temperatura_valor" varchar(50) NOT NULL,
    "conductividad_nivel" varchar(50) NOT NULL,
    "turbidez_nivel" varchar(50) NOT NULL,
    "turbidez_valor" varchar(50) NOT NULL,
    "sistema_sensor" varchar(100) NOT NULL,
    "sensor_detectado" varchar(100) NOT NULL,
    "sensor_nivel" varchar(100) NOT NULL,
    "sensor_valor" varchar(50) NOT NULL,
    "tiempo_resolucion" integer,
    "riesgo_peces" boolean NOT NULL,
    "perdida_economica" boolean NOT NULL,
    "riesgo_personas" boolean NOT NULL,
    "observacion" text NOT NULL,
    "operario_contacto_id" integer REFERENCES "incidencias_operario" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipo_incidencia_normalizada" varchar(100) NOT NULL
);

CREATE TABLE "incidencias_controldiario" (
    "id" serial PRIMARY KEY,
    "fecha" date NOT NULL,
    "anio" integer NOT NULL,
    "semana" integer NOT NULL,
    "dia" varchar(20) NOT NULL,
    "responsable" varchar(200) NOT NULL,
    "modulo" varchar(100) NOT NULL,
    "hora_00_temp" decimal(5, 2),
    "hora_00_ph" decimal(4, 2),
    "hora_00_oxigeno" decimal(5, 2),
    "hora_04_temp" decimal(5, 2),
    "hora_04_ph" decimal(4, 2),
    "hora_04_oxigeno" decimal(5, 2),
    "hora_08_temp" decimal(5, 2),
    "hora_08_ph" decimal(4, 2),
    "hora_08_oxigeno" decimal(5, 2),
    "hora_12_temp" decimal(5, 2),
    "hora_12_ph" decimal(4, 2),
    "hora_12_oxigeno" decimal(5, 2),
    "hora_16_temp" decimal(5, 2),
    "hora_16_ph" decimal(4, 2),
    "hora_16_oxigeno" decimal(5, 2),
    "hora_20_temp" decimal(5, 2),
    "hora_20_ph" decimal(4, 2),
    "hora_20_oxigeno" decimal(5, 2),
    "promedio_temp" decimal(5, 2),
    "promedio_ph" decimal(4, 2),
    "promedio_oxigeno" decimal(5, 2),
    "creado_en" timestamptz NOT NULL,
    "actualizado_en" timestamptz NOT NULL,
    "centro_id" varchar(50) NOT NULL REFERENCES "incidencias_centro" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("centro_id", "fecha", "modulo")
);

CREATE TABLE "incidencias_reportecamaras" (
    "id" serial PRIMARY KEY,
    "fecha" date NOT NULL,
    "turno" varchar(20) NOT NULL,
    "responsable" varchar(200) NOT NULL,
    "rio_pescado_tiene_incidencias" boolean NOT NULL,
    "rio_pescado_descripcion" text NOT NULL,
    "collin_tiene_incidencias" boolean NOT NULL,
    "collin_descripcion" text NOT NULL,
    "lican_tiene_incidencias" boolean NOT NULL,
    "lican_descripcion" text NOT NULL,
    "trafun_tiene_incidencias" boolean NOT NULL,
    "trafun_descripcion" text NOT NULL,
    "creado_en" timestamptz NOT NULL,
    "actualizado_en" timestamptz NOT NULL,
    UNIQUE ("fecha", "turno")
);

-- MIGRACIONES COMPLETADAS
CREATE TABLE "django_migrations" (
    "id" serial PRIMARY KEY,
    "app" varchar(255) NOT NULL,
    "name" varchar(255) NOT NULL,
    "applied" timestamptz NOT NULL
);

INSERT INTO django_migrations (app, name, applied) VALUES
('contenttypes', '0001_initial', NOW()),
('auth', '0001_initial', NOW()),
('auth', '0002_alter_permission_name_max_length', NOW()),
('auth', '0003_alter_user_email_max_length', NOW()),
('auth', '0004_alter_user_username_opts', NOW()),
('auth', '0005_alter_user_last_login_null', NOW()),
('auth', '0006_require_contenttypes_0002', NOW()),
('auth', '0007_alter_validators_add_error_messages', NOW()),
('auth', '0008_alter_user_username_max_length', NOW()),
('auth', '0009_alter_user_last_name_max_length', NOW()),
('auth', '0010_alter_group_name_max_length', NOW()),
('auth', '0011_update_proxy_permissions', NOW()),
('auth', '0012_alter_user_first_name_max_length', NOW()),
('incidencias', '0001_initial', NOW()),
('incidencias', '0002_operario_incidencia_tipo_incidencia_normalizada_and_more', NOW()),
('incidencias', '0003_add_slug_field', NOW()),
('incidencias', '0004_controldiario', NOW()),
('incidencias', '0005_reportecamaras_controldiario_modulo_and_more', NOW()),
('incidencias', '0006_alter_reportecamaras_options_and_more', NOW()),
('sessions', '0001_initial', NOW());

-- USUARIO ADMIN
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES (1, 'pbkdf2_sha256$600000$gIeA90iXunNoN7MhX7H7$F3Msh/5C3Fv/5C3Fv/5C3Fv/5C3Fv/5C3Fv/5C3Fv/5I=', NOW(), true, 'admin', 'Admin', 'Cermaq', 'admin@cermaq.com', true, true, NOW());

SELECT 'Tablas y Admin Creados' as Status;
