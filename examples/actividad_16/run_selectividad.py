# %% [MOTOR REBT: JERARQUÍA, IMPEDANCIAS Y SELECTIVIDAD]
import math

class BloqueCypelec:
    def __init__(self, nombre, p_kw, L, S, Z_prev=6.04+19.2j, In=10, Icu=1.5, tipo="Instalación interior"):
        self.nombre = nombre
        self.p_kw = p_kw
        self.L = L
        self.S = S
        self.Z_prev = Z_prev
        self.In = In
        self.Icu = Icu
        self.tipo = tipo
        
        # Constantes físicas REBT
        self.rho_20 = 0.018
        self.alpha = 0.00392
        self.X_u = 0.000123 # Reactancia mOhm/m
        self.V = 230.0
        
        self.calcular_bloque()

    def calcular_bloque(self):
        # Impedancias propias (mOhm)[cite: 4]
        r20 = (self.rho_20 * self.L / self.S) * 1000
        x = self.X_u * self.L * 1000
        self.z_cab_20 = complex(r20, x)
        self.z_cab_160 = complex(r20 * (1 + self.alpha * 140), x) # 160°C[cite: 4]
        self.z_cab_70 = complex(r20 * (1 + self.alpha * 50), x)  # 70°C[cite: 4]
        
        # Impedancia total en el pie[cite: 4]
        self.Z_pie_20 = self.Z_prev + self.z_cab_20
        self.Z_pie_160 = self.Z_prev + self.z_cab_160
        
        # Cortocircuitos (kA)[cite: 4]
        self.Ik1_max_cab = (1.05 * self.V) / abs(self.Z_prev)
        self.Ik1_max_pie = (1.05 * self.V) / abs(self.Z_pie_20)
        self.Ik1_min_pie = (0.95 * self.V) / abs(self.Z_pie_160)
        
        # Resultados[cite: 4]
        self.ib = (self.p_kw * 1000) / self.V
        self.du_pct = (2 * self.L * 0.021 * self.ib / self.S) / self.V * 100

    def imprimir_burbuja(self, du_acum):
        print(f"\n{'-'*50}")
        print(f"{self.nombre.upper()}")
        print(f"{'-'*50}")
        print(f"Referencia : {self.nombre}")
        print(f"{self.tipo} | Tipo: B1")
        
        print(f"\nImpedancia del cable (mOhm)")
        print(f"Z(1)20º  : {self.z_cab_20.real:.2f} + j {self.z_cab_20.imag:.2f}")
        print(f"Z(1)70º  : {self.z_cab_70.real:.2f} + j {self.z_cab_70.imag:.2f}")
        print(f"Z(1)160º : {self.z_cab_160.real:.2f} + j {self.z_cab_160.imag:.2f}")
        
        print(f"\nCorrientes de cortocircuito (kA)")
        print(f"Cabecera máx: {self.Ik1_max_cab:.2f} | Pie máx: {self.Ik1_max_pie:.2f}")
        print(f"Pie mín     : {self.Ik1_min_pie:.2f}")
        
        print(f"\nResultados")
        print(f"IB: {self.ib:.2f} A | Iz: 15.22 A | In: {self.In} A")
        print(f"dU: {self.du_pct:.2f} % | dUac: {du_acum:.2f} %")
        print(f"{'-'*50}")

def verificar_selectividad(protecciones):
    print("\nREPORTE DE SELECTIVIDAD (AMPERIMÉTRICA)")
    print("-" * 50)
    for i in range(len(protecciones)-1):
        aguas_arriba = protecciones[i]
        aguas_abajo = protecciones[i+1]
        # Regla general REBT: In_superior >= 1.6 * In_inferior para selectividad total
        ratio = aguas_arriba / aguas_abajo
        estado = "OK" if ratio >= 1.6 else "WARNING (Parcial)"
        print(f"{aguas_arriba}A -> {aguas_abajo}A | Ratio: {ratio:.2f} | Estado: {estado}")

# %% [EJECUCIÓN]
if __name__ == "__main__":
    # 1. Suministro (CGBT)
    cgbt = BloqueCypelec("Suministro (CGBT)", 0.20, 10, 1.5, Z_prev=6.04+19.2j, In=25)
    
    # 2. Línea Intermedia
    linea = BloqueCypelec("Línea", 0.20, 10, 1.5, Z_prev=cgbt.Z_pie_20, In=10)
    
    # 3. Circuito C1
    c1 = BloqueCypelec("Circuito C1", 0.20, 20, 1.5, Z_prev=linea.Z_pie_20, In=6)
    
    # Imprimir Reportes
    prog_du = 0
    tramos = [cgbt, linea, c1]
    for t in tramos:
        prog_du += t.du_pct
        t.imprimir_burbuja(prog_du)
    
    # Verificar Jerarquía de Protecciones[cite: 2, 3]
    verificar_selectividad([25, 10, 6])