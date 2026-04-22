# %% Celda 1: Compilación de la Base de Datos DuckDB (Actividad 07)
import duckdb
import pandas as pd

def actualizar_normativas_duckdb(db_path: str):
    SHEET_ID = "13VgjtU85yvMW02NLisRsmJ_LdGqg_h75oIn1sKe2Hks"

    # GIDs proporcionados
    gids = {
        "intensidades_sub": "1356593487",
        "secciones_neutro": "390047301",
        "diametros_tubos": "1429167500"
    }

    print("Descargando tablas normativas desde Google Sheets...")

    dfs = {}
    for nombre, gid in gids.items():
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        try:
            df = pd.read_csv(url)
            df.columns = df.columns.str.strip()  # Limpiar espacios
            dfs[nombre] = df
            print(f" -> Tabla '{nombre}' descargada ({len(df)} filas).")
        except Exception as e:
            print(f"❌ Error al descargar {nombre}: {e}")
            return

    import os

    # 1. Asegurar que el directorio de la base de datos existe
    # Si la carpeta 'db' no existe, esto la crea. Si ya existe, no hace nada.
    directorio = os.path.dirname(db_path)
    if directorio:  # Solo intenta crear si hay una ruta de directorio válida
        os.makedirs(directorio, exist_ok=True)

    # Inyectar en DuckDB
    with duckdb.connect(db_path) as db:
        # 2. Extraer los dataframes a variables locales simples
        # (DuckDB necesita nombres de variables directos, no llamadas a diccionarios)
        df_intensidades = dfs['intensidades_sub']
        df_neutros = dfs['secciones_neutro']
        df_tubos = dfs['diametros_tubos']

        # 1. Tabla de Intensidades Subterráneas
        db.execute("DROP TABLE IF EXISTS intensidades_subterraneas")
        db.execute("""
                CREATE TABLE intensidades_subterraneas (
                    id_sistema VARCHAR, seccion_mm2 DOUBLE, 
                    material VARCHAR, aislamiento VARCHAR, intensidad_A DOUBLE
                )
            """)
        db.execute("INSERT INTO intensidades_subterraneas SELECT * FROM df_intensidades")

        # 2. Tabla de Secciones de Neutro
        db.execute("DROP TABLE IF EXISTS secciones_neutro")
        db.execute("""
                CREATE TABLE secciones_neutro (
                    seccion_fase_mm2 DOUBLE PRIMARY KEY, seccion_neutro_mm2 DOUBLE
                )
            """)
        db.execute("INSERT INTO secciones_neutro SELECT * FROM df_neutros")

        # 3. Tabla de Diámetros de Tubos
        db.execute("DROP TABLE IF EXISTS diametros_tubos")
        db.execute("""
                CREATE TABLE diametros_tubos (
                    id_sistema VARCHAR, seccion_fase_mm2 DOUBLE, diametro_minimo_mm DOUBLE
                )
            """)
        db.execute("INSERT INTO diametros_tubos SELECT * FROM df_tubos")

    print(f"✅ Base de datos '{db_path}' actualizada y lista para calcular.")

# Ejecutar la actualización
import os
DB_PATH = os.path.join(r'C:\dev\residential-energy-efficiency-stats\db', 'normativas.duckdb')
actualizar_normativas_duckdb(DB_PATH)