#%% setup
import os
import sys
print(os.getcwd())
from pprint import pprint

# Add parent directory to path if running directly
if os.path.basename(os.getcwd()) == 'actividad_06':
    sys.path.insert(0, os.path.dirname(os.getcwd()))

#%% Ejecutar validación

from validar_datos import cargar_y_validar_datos

datos_actividad_6 = cargar_y_validar_datos(ruta_json=r'data.json')
pprint(datos_actividad_6.model_dump_json())

#%% calcular resultados
from motor_calculo import MotorCalculoLGA
# ==========================================
# 3. EJECUCIÓN DEL PIPELINE
# ==========================================
# Simulación de los datos validados por Pydantic que entran al motor
# datos_actividad_6 = {
#     "proyecto": {"prevision_carga_W": 145000, "tipo_acometida": "subterranea", "cos_phi": 0.9},
#     "lga": {"sistema_instalacion": "B1", "temperatura_ambiente_C": 45, "longitud_m": 40.0, "conductividad_c": 44.0}
# }

# (Asegúrate de que normativas.duckdb está en el directorio)
motor = MotorCalculoLGA(r'normativas.duckdb')

try:
    informe_final = motor.calcular_lga(datos_actividad_6)
    pprint(informe_final)
    print("\n--- INFORME DE AUDITORÍA LGA (ACTIVIDAD 6) ---")
    for clave, resultado in informe_final.items():
        print(f"\n[{clave.upper()}] : {resultado.valor} {resultado.unidad}")
        print(f"  > Norma: {resultado.normativa} | Criterio: {resultado.criterio}")
        print(f"  > Traza: {resultado.trazabilidad}")

except Exception as e:
    print(f"Error en el motor de cálculo: {e}")