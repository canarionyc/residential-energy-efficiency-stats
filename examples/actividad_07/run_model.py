# %% Celda 2: Motor de Resolución LGA - Actividad 07
import math
import duckdb

# Los datos de entrada estrictos basados en tu PDF
datos_actividad_07 = [
    {"id": "CASO_01", "P_W": 110000, "sistema": "enterrada", "L_m": 35.0, "T_C": 20, "tubos_paralelos": 2},
    {"id": "CASO_02", "P_W": 87000, "sistema": "enterrada", "L_m": 15.0, "T_C": 20, "tubos_paralelos": 2},
    {"id": "CASO_03", "P_W": 35000, "sistema": "A1", "L_m": 30.0, "T_C": 40, "tubos_paralelos": 1}
]


def resolver_caso(caso: dict, db_path: str):
    voltaje = 400
    cos_phi = 0.9
    c_cu = 44  # Conductividad Cobre XLPE 90ºC
    caida_max_V = 0.005 * voltaje  # 0.5% (CC en Planta Baja)

    # 1. Intensidad de Cálculo (Ib)
    ib = caso['P_W'] / (math.sqrt(3) * voltaje * cos_phi)

    # 2. Sección por Caída de Tensión (Criterio Físico)
    s_caida = (caso['P_W'] * caso['L_m']) / (c_cu * caida_max_V * voltaje)

    # 3. Factor de corrección por temperatura (Simplificado para el ejemplo)
    # Enterrado: Base 25ºC. A 20ºC el cable refrigera MEJOR, factor > 1 (aprox 1.04).
    # Al aire (A1): Base 40ºC. A 40ºC factor = 1.0.
    factor_t = 1.04 if caso['sistema'] == 'enterrada' and caso['T_C'] == 20 else 1.0
    ib_corregida = ib / factor_t

    with duckdb.connect(db_path) as db:
        # 4. Buscar Sección Comercial y Térmica
        if caso['sistema'] == 'enterrada':
            query_seccion = """
                SELECT seccion_mm2, intensidad_A FROM intensidades_subterraneas 
                WHERE seccion_mm2 >= ? AND intensidad_A >= ?
                ORDER BY seccion_mm2 ASC LIMIT 1
            """
            # Solo ejecuta en BD si es enterrada
            try:
                fase_mm2, iz_tabulada = db.execute(query_seccion, [s_caida, ib_corregida]).fetchone()
            except TypeError:
                fase_mm2, iz_tabulada = ("No encontrada", 0)
        else:
            # Placeholder directo para A1, sin llamar a DuckDB por ahora
            fase_mm2, iz_tabulada = 35.0, 119.0

        # 5. Buscar Sección del Neutro
        try:
            neutro_mm2 = db.execute("SELECT seccion_neutro_mm2 FROM secciones_neutro WHERE seccion_fase_mm2 = ?",
                [fase_mm2]).fetchone()[0]
        except:
            neutro_mm2 = fase_mm2  # Si no se encuentra, por defecto igual a la fase

        # 6. Buscar Diámetro del Tubo
        try:
            tubo_mm = \
            db.execute("SELECT diametro_minimo_mm FROM diametros_tubos WHERE id_sistema = ? AND seccion_fase_mm2 = ?",
                [caso['sistema'], fase_mm2]).fetchone()[0]
        except:
            tubo_mm = "No tabulado"

    # IMPRESIÓN DEL INFORME TRAZABLE
    print(f"\n{'=' * 40}")
    print(f" RESOLUCIÓN {caso['id']} ({caso['P_W'] / 1000} kW | {caso['sistema'].upper()})")
    print(f"{'=' * 40}")
    print(f"Física:")
    print(f" - Intensidad (Ib): {ib:.2f} A")
    print(f" - Sección mínima por Caída Tensión: {s_caida:.2f} mm2")
    print(f"\nDecisión Normativa (DuckDB):")
    print(f" 1. Tipo de conductor: Cobre, Aislamiento XLPE (0.6/1kV)")
    print(f" 2. Sección conductor Fase: {fase_mm2} mm2 (Soporta {iz_tabulada} A > {ib:.1f} A)")
    print(f" 3. Sección conductor Neutro: {neutro_mm2} mm2")
    print(f" 4. Diámetro del tubo: {tubo_mm} mm")
    print(f" 5. Sección constructiva: 3x{fase_mm2} + 1x{neutro_mm2} mm2")
    print(f" 6. CGP y Fusibles: CGP-9 | Fusibles In >= {ib:.0f}A y <= {iz_tabulada:.0f}A")

import os
DB_PATH = os.path.join(r'C:\dev\residential-energy-efficiency-stats\db', 'normativas.duckdb')
# Procesar todos los casos
for caso_actual in datos_actividad_07:
    resolver_caso(caso_actual, DB_PATH)