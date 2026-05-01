# %% [MOTOR REBT COMPLETO: CGBT + LÍNEA + C1]
import math


class TramoElectrico:
    def __init__(self, nombre, p_kw, L, S, Z_red_complex=0j):
        self.nombre = nombre
        self.p_w = p_kw * 1000
        self.L = L
        self.S = seccion = S
        self.V = 230.0

        # Constantes físicas
        self.rho_20 = 0.018
        self.alpha = 0.00392
        self.X_unitaria = 0.000123  # mOhm/m aproximado según capturas

        # Impedancia aguas arriba (Complex)
        self.Z_red = Z_red_complex

        self.calcular_fisica()

    def calcular_fisica(self):
        # 1. Resistencia y Reactancia del cable (mOhm)
        r_20 = (self.rho_20 * self.L / self.S) * 1000
        x_L = self.X_unitaria * self.L * 10  # Basado en 1.23 mOhm para 10m
        self.z_cable_20 = complex(r_20, x_L)

        # Resistencia a 160°C (para Icc min)
        r_160 = r_20 * (1 + self.alpha * (160 - 20))
        self.z_cable_160 = complex(r_160, x_L)

        # 2. Impedancia Total en el punto (mOhm)
        self.Z_total_20 = self.Z_red + self.z_cable_20

        # 3. Corrientes de Cortocircuito (kA)[cite: 5]
        # Ik1 = (c * V) / |2*Z1 + Z0|. Simplificado para monofásico:
        c_max = 1.05
        self.Icc_max = (c_max * self.V) / abs(self.Z_total_20)

        # 4. Caída de tensión individual (%)[cite: 5]
        self.ib = self.p_w / self.V
        rho_servicio = self.rho_20 * (1 + self.alpha * (40 - 20))
        self.du_v = (2 * self.L * rho_servicio * self.ib) / self.S
        self.du_pct = (self.du_v / self.V) * 100


def imprimir_tabla_comparativa(tramos):
    print(f"{'BLOQUE':<15} | {'L (m)':<6} | {'S (mm2)':<7} | {'dU (%)':<7} | {'Icc (kA)':<10}")
    print("-" * 55)
    du_acum = 0
    for t in tramos:
        du_acum += t.du_pct
        print(f"{t.nombre:<15} | {t.L:<6.1f} | {t.S:<7.1f} | {du_acum:<7.2f} | {t.Icc_max:<10.2f}")


# %% [EJECUCIÓN BASADA EN SNAPSHOTS 2, 3 Y 4]
if __name__ == "__main__":
    # 1. Suministro (CGBT) - Snapshot 2[cite: 5]
    # Zq(1) = 6.04 + j19.20 mOhm. Ik1_max = 8.05 kA.
    z_red_inicial = complex(6.04, 19.20)
    cgbt = TramoElectrico("Suministro", 0.20, 10.0, 1.5, z_red_inicial)

    # 2. Línea Intermedia - Snapshot 3[cite: 5]
    # Recibe la impedancia del CGBT. L=10m, S=1.5. Ik1_max = 1.77 kA.
    linea = TramoElectrico("Línea", 0.20, 10.0, 1.5, cgbt.Z_total_20)

    # 3. Circuito C1 - Snapshot 4[cite: 5]
    # Recibe la impedancia de la Línea. L=20m, S=1.5. Ik1_max = 0.94 kA.
    c1 = TramoElectrico("Circuito C1", 0.20, 20.0, 1.5, linea.Z_total_20)

    # Mostrar reporte ASCII unificado
    print("\nREPORTE TÉCNICO DE LA INSTALACIÓN (RESUMEN)")
    imprimir_tabla_comparativa([cgbt, linea, c1])