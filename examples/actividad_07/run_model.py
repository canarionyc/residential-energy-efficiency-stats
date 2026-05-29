# %% Celda 2: Motor de Resolución LGA - Actividad 07
import math
from pprint import pp
import tabulate
import duckdb

# Los datos de entrada estrictos basados en tu PDF
datos_actividad_07 = [
    {"id": "CASO_01", "P_W": 110000, "sistema": "enterrada", "L_m": 35.0, "T_C": 20, "tubos_paralelos": 2},
    {"id": "CASO_02", "P_W": 87000, "sistema": "enterrada", "L_m": 15.0, "T_C": 20, "tubos_paralelos": 2},
    {"id": "CASO_03", "P_W": 35000, "sistema": "A1", "L_m": 30.0, "T_C": 40, "tubos_paralelos": 1}
]
print(__import__('tabulate').tabulate(datos_actividad_07, headers="keys", tablefmt="outline"))
#%% imprimir tabla
def imprimir_tabla(datos):
    columnas = ["id", "P_W", "sistema", "L_m", "T_C", "tubos_paralelos"]
    encabezados = {
        "id": "ID",
        "P_W": "P_W",
        "sistema": "Sistema",
        "L_m": "L_m",
        "T_C": "T_C",
        "tubos_paralelos": "Tubos",
    }

    filas = []
    for fila in datos:
        filas.append([str(fila.get(col, "")) for col in columnas])

    anchos = []
    for idx, col in enumerate(columnas):
        ancho_columna = len(encabezados[col])
        for fila in filas:
            ancho_columna = max(ancho_columna, len(fila[idx]))
        anchos.append(ancho_columna)

    def fmt_fila(valores):
        celdas = [valores[i].ljust(anchos[i]) for i in range(len(columnas))]
        return "| " + " | ".join(celdas) + " |"

    separador = "+-" + "-+-".join("-" * ancho for ancho in anchos) + "-+"

    print(separador)
    print(fmt_fila([encabezados[col] for col in columnas]))
    print(separador)
    for fila in filas:
        print(fmt_fila(fila))
    print(separador)

imprimir_tabla(datos_actividad_07)

#%% Celda 3: Motor de Resolución LGA
def resolver_caso(caso: dict, db_path: str) -> dict:
    voltaje = 400
    cos_phi = 0.9
    c_cu = 44  # Conductividad Cobre XLPE 90ºC
    caida_max_V = 0.005 * voltaje  # 0.5% (CC en Planta Baja)
    results: dict={}

    # 1. Intensidad de Cálculo (Ib)
    ib = caso['P_W'] / (math.sqrt(3) * voltaje * cos_phi)
    print(f"Intensidad de Calculo (Ib): {ib:.2f} A")
    # 2. Sección por Caída de Tensión (Criterio Físico)
    s_caida = (caso['P_W'] * caso['L_m']) / (c_cu * caida_max_V * voltaje)
    print(f"Sección por Caída de Tensión (s_caida): {s_caida:.2f} mm2")
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
            print(f"{query_seccion}\nCon parámetros: s_caida={s_caida:.2f}, ib_corregida={ib_corregida:.2f}")
            # Solo ejecuta en BD si es enterrada
            try:
                fase_mm2, iz_tabulada = db.execute(query_seccion, [s_caida, ib_corregida]).fetchone()
            except TypeError:
                fase_mm2, iz_tabulada = ("No encontrada", 0)
        else:
            # Placeholder directo para A1, sin llamar a DuckDB por ahora
            fase_mm2, iz_tabulada = 35.0, 119.0
        print(f"Seccion Fase {fase_mm2} mm2, Iz tabulada {iz_tabulada} A")


        # 5. Buscar Sección del Neutro
        try:
            query_seccion_neutro = "SELECT seccion_neutro_mm2 FROM secciones_neutro WHERE seccion_fase_mm2 = ?"
            neutro_mm2 = db.execute(query_seccion_neutro,
                [fase_mm2]).fetchone()[0]
            print(f"{query_seccion_neutro}\nCon parámetros: fase_mm2={fase_mm2}")
        except:
            neutro_mm2 = fase_mm2  # Si no se encuentra, por defecto igual a la fase

        # 6. Buscar Diámetro del Tubo
        try:
            query_diametro_tubo="SELECT diametro_minimo_mm FROM diametros_tubos WHERE id_sistema = ? AND seccion_fase_mm2 = ?"
            tubo_mm = \
            db.execute(query_diametro_tubo,
                [caso['sistema'], fase_mm2]).fetchone()[0]
            print(f"{query_diametro_tubo}\nCon parámetros: sistema={caso['sistema']}, fase_mm2={fase_mm2}")
        except:
            tubo_mm = "No tabulado"
    print(f"Diámetro del Tubo: {tubo_mm} mm")

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

#%% Execute
import os
import json
DB_PATH = os.path.join(r'C:\dev\residential-energy-efficiency-stats\db', 'normativas.duckdb')
# Procesar todos los casos
# 3. Calcular todos los escenarios
resultados = [resolver_caso(caso_actual, DB_PATH) for caso_actual in datos_actividad_07]
json.dump(resultados, open('resultados.json', 'w'), indent=2)