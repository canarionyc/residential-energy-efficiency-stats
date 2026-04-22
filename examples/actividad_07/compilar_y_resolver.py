# %% SCRIPT MAESTRO: INGESTIÓN Y MOTOR DE CÁLCULO (ACTIVIDAD 07)
import json
import os
import math
import duckdb
import pandas as pd


# ==========================================
# 1. ACTUALIZACIÓN DE LA BASE DE DATOS
# ==========================================
def compilar_base_de_datos(db_path: str):
    SHEET_ID = "13VgjtU85yvMW02NLisRsmJ_LdGqg_h75oIn1sKe2Hks"

    gids = {
        "intensidades_sub": "1356593487",
        "secciones_neutro": "390047301",
        "diametros_tubos": "1429167500",
        "intensidades_sup": "647499519"
    }

    print("📥 Descargando tablas normativas desde Google Sheets...")
    dfs = {}
    for nombre, gid in gids.items():
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        try:
            df = pd.read_csv(url)
            df.columns = df.columns.str.strip()
            dfs[nombre] = df
            print(f"  -> {nombre} OK ({len(df)} filas)")
        except Exception as e:
            print(f"❌ Error crítico descargando {nombre}: {e}")
            return

    # Asegurar que el directorio de la DB existe
    directorio = os.path.dirname(db_path)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    print("🏗️ Compilando DuckDB local...")
    with duckdb.connect(db_path) as db:
        df_sub = dfs['intensidades_sub']
        df_neu = dfs['secciones_neutro']
        df_tub = dfs['diametros_tubos']
        df_sup = dfs['intensidades_sup']

        # Tabla 1: Subterráneas
        db.execute("DROP TABLE IF EXISTS intensidades_subterraneas")
        db.execute(
            "CREATE TABLE intensidades_subterraneas (id_sistema VARCHAR, seccion_mm2 DOUBLE, material VARCHAR, aislamiento VARCHAR, intensidad_A DOUBLE)")
        db.execute("INSERT INTO intensidades_subterraneas SELECT * FROM df_sub")

        # Tabla 2: Neutros
        db.execute("DROP TABLE IF EXISTS secciones_neutro")
        db.execute("CREATE TABLE secciones_neutro (seccion_fase_mm2 DOUBLE PRIMARY KEY, seccion_neutro_mm2 DOUBLE)")
        db.execute("INSERT INTO secciones_neutro SELECT * FROM df_neu")

        # Tabla 3: Tubos
        db.execute("DROP TABLE IF EXISTS diametros_tubos")
        db.execute(
            "CREATE TABLE diametros_tubos (id_sistema VARCHAR, seccion_fase_mm2 DOUBLE, diametro_minimo_mm DOUBLE)")
        db.execute("INSERT INTO diametros_tubos SELECT * FROM df_tub")

        # Tabla 4: Superficie (NUEVA)
        db.execute("DROP TABLE IF EXISTS intensidades_superficie")
        db.execute(
            "CREATE TABLE intensidades_superficie (id_sistema VARCHAR, seccion_mm2 DOUBLE, material VARCHAR, aislamiento VARCHAR, intensidad_A DOUBLE)")
        db.execute("INSERT INTO intensidades_superficie SELECT * FROM df_sup")

    print(f"✅ Base de datos compilada exitosamente en: {db_path}\n")


# ==========================================
# 2. MOTOR DE RESOLUCIÓN (TRACEABLE ENGINE)
# ==========================================
def resolver_caso(caso: dict, db_path: str) -> dict:
    voltaje = 400
    cos_phi = 0.9
    c_cu = 44  # Cobre XLPE 90ºC
    caida_max_V = 0.005 * voltaje  # 0.5% (CC en Planta Baja)

    # 1. Física Pura
    ib = caso['P_W'] / (math.sqrt(3) * voltaje * cos_phi)
    s_caida = (caso['P_W'] * caso['L_m']) / (c_cu * caida_max_V * voltaje)

    # Factor térmico
    factor_t = 1.04 if caso['sistema'] == 'enterrada' and caso['T_C'] == 20 else 1.0
    ib_corregida = ib / factor_t

    # 2. Consultas a la Normativa
    with duckdb.connect(db_path) as db:
        # A. Seleccionar la tabla de intensidades adecuada según el sistema
        if caso['sistema'] == 'enterrada':
            query_seccion = """
                SELECT seccion_mm2, intensidad_A FROM intensidades_subterraneas 
                WHERE seccion_mm2 >= ? AND intensidad_A >= ?
                ORDER BY seccion_mm2 ASC LIMIT 1
            """
        else:  # Para A1 y otros de superficie
            query_seccion = """
                SELECT seccion_mm2, intensidad_A FROM intensidades_superficie 
                WHERE id_sistema = ? AND seccion_mm2 >= ? AND intensidad_A >= ?
                ORDER BY seccion_mm2 ASC LIMIT 1
            """

        try:
            if caso['sistema'] == 'enterrada':
                fase_mm2, iz_tabulada = db.execute(query_seccion, [s_caida, ib_corregida]).fetchone()
            else:
                fase_mm2, iz_tabulada = db.execute(query_seccion, [caso['sistema'], s_caida, ib_corregida]).fetchone()
        except TypeError:
            fase_mm2, iz_tabulada = ("No encontrada", 0)

        # B. Buscar Neutro
        try:
            neutro_mm2 = db.execute("SELECT seccion_neutro_mm2 FROM secciones_neutro WHERE seccion_fase_mm2 = ?",
                [fase_mm2]).fetchone()[0]
        except:
            neutro_mm2 = fase_mm2

        # C. Buscar Tubo
        try:
            tubo_mm = \
            db.execute("SELECT diametro_minimo_mm FROM diametros_tubos WHERE id_sistema = ? AND seccion_fase_mm2 = ?",
                [caso['sistema'], fase_mm2]).fetchone()[0]
        except:
            tubo_mm = "No tabulado"

    # 3. Emisión del Dictamen
    print(f"{'=' * 45}")
    print(f" RESOLUCIÓN {caso['id']} ({caso['P_W'] / 1000} kW | SISTEMA: {caso['sistema'].upper()})")
    print(f"{'=' * 45}")
    print("Criterios de Diseño (Física):")
    print(f"  • Intensidad real (Ib): {ib:.2f} A")
    print(f"  • Sección mínima por caída de tensión: {s_caida:.2f} mm2")
    print("\nAplicación Normativa (REBT):")
    print(f"  1. Tipo conductor : Cobre, Aislamiento XLPE/EPR (0.6/1kV)")
    print(f"  2. Sección Fase   : {fase_mm2} mm2 (Soporta térmicamente {iz_tabulada} A > {ib:.1f} A)")
    print(f"  3. Sección Neutro : {neutro_mm2} mm2")
    print(f"  4. Diámetro tubo  : {tubo_mm} mm")
    print(f"  5. Solución final : 3x{fase_mm2} + 1x{neutro_mm2} mm2")
    print(f"  6. CGP y Fusibles : CGP-9 | Fusibles In entre {math.ceil(ib)}A y {math.floor(iz_tabulada)}A\n")

    # Return a structured dictionary instead of printing
    return {
        "id": caso['id'].replace('_', ' '),
        "potencia_kW": caso['P_W'] / 1000,
        "sistema": caso['sistema'].upper(),
        "ib_A": round(ib, 2),
        "s_caida_mm2": round(s_caida, 2),
        "fase_mm2": fase_mm2,
        "iz_A": iz_tabulada,
        "neutro_mm2": neutro_mm2,
        "tubo_mm": tubo_mm,
        "in_min_A": math.ceil(ib),
        "in_max_A": math.floor(iz_tabulada)
    }


# ==========================================
# 3. EJECUCIÓN DEL PIPELINE
# ==========================================
if __name__ == "__main__":
    DB_PATH = os.path.join('db', 'normativas.duckdb')

    # 1. Sincronizar bases de datos (si cambias algún valor en la nube, se reflejará aquí)
    compilar_base_de_datos(DB_PATH)

    # 2. Los datos puros del PDF (Actividad 07)
    datos_actividad_07 = [
        {"id": "CASO_01", "P_W": 110000, "sistema": "enterrada", "L_m": 35.0, "T_C": 20},
        {"id": "CASO_02", "P_W": 87000, "sistema": "enterrada", "L_m": 15.0, "T_C": 20},
        {"id": "CASO_03", "P_W": 35000, "sistema": "A1", "L_m": 30.0, "T_C": 40}
    ]

    # 3. Calcular todos los escenarios
    resultados = [resolver_caso(caso_actual, DB_PATH)  for caso_actual in datos_actividad_07]
    json.dump(resultados, open('resultados.json', 'w'), indent=2)