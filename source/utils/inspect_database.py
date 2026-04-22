#%%
import duckdb
import pandas as pd

db_path = 'db/normativas.duckdb'

with duckdb.connect(db_path) as db:
    # 1. Obtener la lista de todas las tablas de usuario
    tablas = db.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'main'
    """).fetchall()

    print("========================================")
    print(f"📦 INSPECCIÓN DE LA BASE DE DATOS")
    print("========================================\n")

    if not tablas:
        print("La base de datos está vacía.")

    # 2. Iterar sobre cada tabla e imprimir su contenido
    for tabla_tuple in tablas:
        nombre_tabla = tabla_tuple[0]
        print(f"--- TABLA: {nombre_tabla.upper()} ---")

        # DuckDB permite extraer directamente a un DataFrame de Pandas (.df())
        # LIMIT 10 por si alguna tabla fuera gigantesca (aquí son pequeñas)
        df = db.execute(f"SELECT * FROM {nombre_tabla} LIMIT 10").df()

        # Imprimir la tabla formateada
        print(df.to_string(index=False))
        print("\n")