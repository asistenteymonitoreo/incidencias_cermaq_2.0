import sqlite3

# Conectar a SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("📊 Tablas en la base de datos SQLite:\n")

for table in tables:
    table_name = table[0]
    
    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"✓ {table_name}: {count} registros")
        
        # Mostrar estructura de las tablas con datos
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"  Columnas: {', '.join([col[1] for col in columns])}")
        print()

conn.close()
