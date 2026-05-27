from pydantic import BaseModel
from typing import Dict, Any


# ==========================================
# 1. CLASE DE RESULTADO TRAZABLE (Audit Trail)
# ==========================================
class TraceableResult(BaseModel):
    valor: Any
    unidad: str
    criterio: str
    normativa: str
    trazabilidad: str