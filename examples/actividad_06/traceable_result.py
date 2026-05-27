from pydantic import BaseModel
from typing import Any


# ==========================================
# 1. CLASE DE RESULTADO TRAZABLE (Audit Trail)
# ==========================================
class TraceableResult(BaseModel):
    valor: Any
    unidad: str
    criterio: str
    normativa: str
    trazabilidad: str

    def __str__(self) -> str:
        return f"{self.valor} {self.unidad} | {self.criterio} | {self.normativa}"

    def __repr__(self) -> str:
        return f"{self.valor} {self.unidad} | {self.criterio} | {self.normativa}"

    def __dir__(self) -> str:
        return (
            "TraceableResult(\n"
            f"  valor={self.valor!r},\n"
            f"  unidad={self.unidad!r},\n"
            f"  criterio={self.criterio!r},\n"
            f"  normativa={self.normativa!r},\n"
            f"  trazabilidad={self.trazabilidad!r}\n"
            ")"
        )