# %% [MOTOR FÍSICO REBT - FUENTE DE VERDAD: COMPROBACIONES_060430]
import math


class MotorCalculoREBT:
    def __init__(self, nombre, p_kw, longitud, seccion, tension=230.0):
        self.nombre = nombre
        self.p_w = p_kw * 1000
        self.L = longitud
        self.S = seccion
        self.V = tension

        # Constantes extraídas del documento
        self.rho_20 = 0.018  # Resistividad Cu a 20°C
        self.alpha = 0.00392  # Coeficiente temperatura Cu
        self.k_aislamiento = 115  # Factor k para PVC

        self.ejecutar_calculos()

    def ejecutar_calculos(self):
        # 1. Intensidad de diseño (Ib)
        self.ib = self.p_w / self.V  # cos phi = 1.00[cite: 5]

        # 2. Resistencia a 20°C (RL20)[cite: 5]
        # RL = rho * (L / S). Para cortocircuito se usa longitud simple.
        self.r_l20 = (self.rho_20 * self.L) / self.S
        self.r_l20_mohm = self.r_l20 * 1000  # Convertir a mOhm para la tabla

        # 3. Resistencia a final de cortocircuito (160°C para PVC)[cite: 5]
        # RL = [1 + alpha * (160 - 20)] * RL20
        self.r_l160 = (1 + self.alpha * (160 - 20)) * self.r_l20
        self.r_l160_mohm = self.r_l160 * 1000

        # 4. Caída de Tensión (dU)[cite: 5]
        # En monofásico: dU = 2 * L * rho * I / S
        # Usamos rho corregido a temperatura de servicio (~40°C en el doc)
        rho_servicio = self.rho_20 * (1 + self.alpha * (40.10 - 20))
        self.du_v = (2 * self.L * rho_servicio * self.ib) / self.S
        self.du_pct = (self.du_v / self.V) * 100

    def imprimir_tabla_impedancias(self):
        print(f"\n--- IMPEDANCIA DEL CABLE: {self.nombre} ---")
        print("-" * 65)
        print(f"| {'Descripción':<25} | {'S (mm2)':<8} | {'Valor (mOhm)':<15} |")
        print("-" * 65)
        print(f"| {'Resistencia a 20°C':<25} | {self.S:<8.2f} | {self.r_l20_mohm:<15.2f} |")
        print(f"| {'Resistencia a 160°C':<25} | {self.S:<8.2f} | {self.r_l160_mohm:<15.2f} |")
        print("-" * 65)


# %% [EJECUCIÓN CON DATOS DE LA FICHA]
if __name__ == "__main__":
    # Datos C1: 0.20 kW, 10m, 1.5mm2[cite: 5]
    circuito_c1 = MotorCalculoREBT(
        nombre="C1 - Alumbrado",
        p_kw=0.20,
        longitud=10.0,
        seccion=1.5
    )

    # Validamos contra la Ficha de Cálculo[cite: 5]
    # Esperado RL20: 120.00 mOhm
    # Esperado RL160: 185.86 mOhm
    circuito_c1.imprimir_tabla_impedancias()

    print(f"\nVerificación dU: {circuito_c1.du_v:.3f} V ({circuito_c1.du_pct:.2f}%)")
    # El doc indica 0.230 V (0.10%)[cite: 5]