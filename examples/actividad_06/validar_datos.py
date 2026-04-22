# %% Celda 1: Esquema Estricto de Datos (Validación Pydantic)
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from typing import Literal
import json

from pydantic import BaseModel, Field, field_validator
import duckdb


class LGAInput(BaseModel):
    # Notice: It's just a string now. The code doesn't know what 'B1' is.
    sistema_instalacion: str
    temperatura_ambiente_C: float = Field(ge=-20, le=90)
    longitud_m: float = Field(gt=0.0)

    @field_validator('sistema_instalacion')
    @classmethod
    def validar_sistema_contra_db(cls, v: str) -> str:
        """Queries DuckDB to verify the system exists in the norm."""
        # Query the database for the provided value
        query = "SELECT descripcion FROM metodos_instalacion WHERE id = ?"
        resultado = db.execute(query, [v.upper()]).fetchone()

        if not resultado:
            # If we dynamically fetch the allowed list for the error message
            permitidos = [row[0] for row in db.execute("SELECT id FROM metodos_instalacion").fetchall()]
            raise ValueError(
                f"Sistema '{v}' no reconocido por la normativa actual. "
                f"Sistemas válidos en la base de datos: {permitidos}"
            )
        return v.upper()


# --- TEST IT ---
#%% 1. Valid Input
db = duckdb.connect(r'normas.db', read_only=True)
datos_validos = {"sistema_instalacion": "B1", "temperatura_ambiente_C": 45, "longitud_m": 40}
lga = LGAInput(**datos_validos)
print(f"✅ Validated: {lga.sistema_instalacion}")

# 2. Invalid Input (Will trigger a dynamic error)
try:
    datos_invalidos = {"sistema_instalacion": "Z9", "temperatura_ambiente_C": 45, "longitud_m": 40}
    LGAInput(**datos_invalidos)
except ValueError as e:
    print(f"❌ Validation Blocked:\n{e}")
# ---------------------------------------------------------
# MODELOS PYDANTIC (Restringen silencios y errores)
# ---------------------------------------------------------
class ProyectoInput(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Prohíbe llaves fantasma en el JSON

    prevision_carga_W: float = Field(gt=0, description="Carga en vatios (W)")
    tipo_acometida: Literal["subterranea", "aerea"]
    cos_phi: float = Field(ge=0.0, le=1.0, description="Factor de potencia")


class LGAInput(BaseModel):
    model_config = ConfigDict(extra='forbid')

    # Restringimos a los métodos de instalación de la UNE-HD 60364-5-52
    sistema_instalacion: Literal["A1", "A2", "B1", "B2", "C", "D", "E", "F", "G"]
    temperatura_ambiente_C: float = Field(ge=-20, le=90)
    longitud_m: float = Field(gt=0.0)
    conductividad_c: float = Field(gt=0.0, description="Conductividad a la temperatura máxima de servicio")


class Actividad6Data(BaseModel):
    model_config = ConfigDict(extra='forbid')
    proyecto: ProyectoInput
    lga: LGAInput


# ---------------------------------------------------------
# MOTOR DE CARGA
# ---------------------------------------------------------
def cargar_y_validar_datos(ruta_json: str) -> Actividad6Data:
    """Carga un JSON y lo valida contra el esquema Pydantic."""
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos_crudos = json.load(f)

        # Pydantic valida los tipos, rangos y strings permitidos en este paso
        datos_validados = Actividad6Data(**datos_crudos)
        print("✅ SUCCESS: Datos cargados y validados. Ninguna ambigüedad detectada.")
        return datos_validados

    except FileNotFoundError:
        print(f"❌ ERROR: El archivo '{ruta_json}' no se encontró.")
        raise
    except ValidationError as e:
        print("❌ ERROR DE VALIDACIÓN: El archivo data.json no cumple la especificación.")
        print(e.json(indent=2))
        raise