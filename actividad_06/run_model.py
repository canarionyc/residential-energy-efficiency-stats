#%% setup
import os
print(os.getcwd())

#%% Ejecutar validación

from actividad_06.validar_datos import cargar_y_validar_datos

datos_problema = cargar_y_validar_datos(ruta_json=r'actividad_06/data.json')