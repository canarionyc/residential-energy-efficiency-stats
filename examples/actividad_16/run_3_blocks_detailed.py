# %% [MOTOR REBT CON GENERACIÓN DE BURBUJAS DE DETALLE]
import math

class TramoREBT:
    def __init__(self, nombre, p_kw, L, S, Z_red_prev=0j, tipo="Instalación interior", metodo="B1"):
        self.nombre = nombre
        self.p_kw = p_kw
        self.L = L
        self.S = S
        self.Z_red_prev = Z_red_prev # Impedancia que viene de aguas arriba
        self.tipo = tipo
        self.metodo = metodo
        
        # Parámetros físicos
        self.rho_20 = 0.018
        self.alpha = 0.00392
        self.X_u = 0.000123 # Reactancia unitaria mOhm/m
        self.V = 230.0
        
        self.ejecutar_calculo()

    def ejecutar_calculo(self):
        # Impedancia propia del cable a 20°C (mOhm)
        r20 = (self.rho_20 * self.L / self.S) * 1000
        x = self.X_u * self.L * 1000
        self.z_cable_20 = complex(r20, x)
        
        # Impedancia propia a 160°C
        r160 = r20 * (1 + self.alpha * (160 - 20))
        self.z_cable_160 = complex(r160, x)
        
        # Impedancia total en el PIE del tramo (mOhm)
        self.Z_pie_20 = self.Z_red_prev + self.z_cable_20
        self.Z_pie_160 = self.Z_red_prev + self.z_cable_160
        
        # Corrientes de Cortocircuito (kA)
        c_max = 1.05
        c_min = 0.95
        # En cabecera (usa Z_red_prev)
        self.Icc_max_cab = (c_max * self.V) / abs(self.Z_red_prev) if abs(self.Z_red_prev) > 0 else 0
        # En pie (usa Z_total)
        self.Icc_max_pie = (c_max * self.V) / abs(self.Z_pie_20)
        self.Icc_min_pie = (c_min * self.V) / abs(self.Z_pie_160)
        
        # Resultados resumen[cite: 5]
        self.ib = (self.p_kw * 1000) / self.V
        self.du_v = (2 * self.L * self.rho_20 * 1.08 * self.ib) / self.S # 1.08 factor temp servicio
        self.du_pct = (self.du_v / self.V) * 100

    def imprimir_burbuja(self, du_acum):
        print(f"\n{'='*50}")
        print(f"{self.nombre.upper()}")
        print(f"{'='*50}")
        print(f"Referencia : {self.nombre}")
        print(f"{self.tipo}")
        print(f"Tipo de instalación : {self.metodo}")
        
        print(f"\nImpedancia del cable")
        print(f"Z(1)20º  : {self.z_cable_20.real:.2f} + j {self.z_cable_20.imag:.2f} mOhm")
        print(f"Z(1)160º : {self.z_cable_160.real:.2f} + j {self.z_cable_160.imag:.2f} mOhm")
        
        print(f"\nCorrientes de cortocircuito (kA)")
        print(f"            Ik1 max    Ik1 min")
        print(f"Cabecera :  {self.Icc_max_cab:<10.2f} --")
        print(f"Pie      :  {self.Icc_max_pie:<10.2f} {self.Icc_min_pie:.2f}")
        
        print(f"\nResultados")
        print(f"IB          : {self.ib:.2f} A")
        print(f"Iz          : 15.22 A") # Valor fijo según tu tabla B1 1.5mm2[cite: 5]
        print(f"dU          : {self.du_pct:.2f} %")
        print(f"dUac        : {du_acum:.2f} %")
        print(f"Iccmax      : {self.Icc_max_pie:.2f} kA (Ik1máx pie)")
        print(f"Iccmin      : {self.Icc_min_pie:.2f} kA (Ik1mín pie)")
        print(f"{'='*50}\n")

# %% [EJECUCIÓN DEL REPORTE POR BLOQUES]
if __name__ == "__main__":
    # Impedancia inicial de red en CGBT[cite: 5]
    z_red_cgbt = complex(6.04, 19.20)
    
    # Bloque 1: Suministro (Snapshot 2)[cite: 5]
    cgbt = TramoREBT("Suministro", 0.20, 10.0, 1.5, z_red_cgbt)
    
    # Bloque 2: Línea (Snapshot 3)[cite: 5]
    linea = TramoREBT("Línea", 0.20, 10.0, 1.5, cgbt.Z_pie_20)
    
    # Bloque 3: Circuito C1 (Snapshot 4)[cite: 5]
    c1 = TramoREBT("Circuito C1", 0.20, 20.0, 1.5, linea.Z_pie_20)
    
    # Impresión de las burbujas acumulando dU
    progreso_du = 0
    for tramo in [cgbt, linea, c1]:
        progreso_du += tramo.du_pct
        tramo.imprimir_burbuja(progreso_du)