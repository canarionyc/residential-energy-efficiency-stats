# %% [MOTOR DE COMPROBACIONES REBT]
import matplotlib.pyplot as plt


class CircuitoResidencialREBT:
    def __init__(self, nombre, tension_v, longitud_m, seccion_mm2, potencia_w, tipo_uso, i_n, i_z, lang='ES'):
        self.nombre = nombre
        self.tension_v = tension_v
        self.longitud_m = longitud_m
        self.seccion_mm2 = seccion_mm2
        self.potencia_w = potencia_w
        self.tipo_uso = tipo_uso.lower()  # 'alumbrado' o 'fuerza'

        # Parámetros de protección térmica
        self.i_n = i_n  # Calibre del magnetotérmico (A)
        self.i_z = i_z  # Intensidad máxima admisible del cable (A)

        self.resistividad_cu_20 = 0.018
        self.lang = lang

    def calcular_fisica(self):
        """Calcula los parámetros físicos base del circuito."""
        self.i_b = self.potencia_w / self.tension_v
        self.r_linea = self.resistividad_cu_20 * (2 * self.longitud_m) / self.seccion_mm2
        self.du_v = self.i_b * self.r_linea
        self.du_pct = (self.du_v / self.tension_v) * 100

    def comprobar_rebt(self):
        """Ejecuta las comprobaciones normativas del REBT."""
        self.calcular_fisica()
        comprobaciones = {}

        # 1. Comprobación de Sobrecarga (Termodinámica)
        # El magnetotérmico (In) debe proteger la carga (Ib) y no superar el límite del cable (Iz)
        cumple_sobrecarga = (self.i_b <= self.i_n) and (self.i_n <= self.i_z)
        comprobaciones['Sobrecarga'] = {
            'formula': f"Ib ({self.i_b:.2f}A) <= In ({self.i_n}A) <= Iz ({self.i_z}A)",
            'cumple': cumple_sobrecarga
        }

        # 2. Comprobación de Caída de Tensión (Eficiencia)
        limite_du = 3.0 if self.tipo_uso == 'alumbrado' else 5.0
        cumple_du = self.du_pct <= limite_du
        comprobaciones['Caida_Tension'] = {
            'formula': f"dU% ({self.du_pct:.2f}%) <= Límite ({limite_du}%)",
            'cumple': cumple_du
        }

        return comprobaciones

    def imprimir_informe(self):
        resultados = self.comprobar_rebt()
        print(f"\n--- FICHA DE COMPROBACIONES: {self.nombre} ---")
        for test, datos in resultados.items():
            estado = "CUMPLE" if datos['cumple'] else "NO CUMPLE"
            print(f"[{estado}] {test}: {datos['formula']}")

    def plot_resultados(self):
        """Genera el gráfico del circuito basado en JSON para fácil traducción."""
        grafico_json = {
            'EN': {
                'title': f'Voltage Drop Analysis - {self.nombre}',
                'axes': ['Source', 'Load'],
                'labels': 'Voltage (V)',
                'annotations': f'Drop: {self.du_pct:.2f}%'
            },
            'ES': {
                'title': f'Análisis de Caída de Tensión - {self.nombre}',
                'axes': ['Origen', 'Carga'],
                'labels': 'Tensión (V)',
                'annotations': f'Caída: {self.du_pct:.2f}%'
            }
        }

        # Selección de idioma a través de la variable de clase
        t = grafico_json[self.lang]

        tensiones = [self.tension_v, self.tension_v - self.du_v]

        plt.figure(figsize=(6, 4))
        barras = plt.bar(t['axes'], tensiones, color=['#2ca02c', '#d62728'])
        plt.ylim(self.tension_v - (self.du_v * 2) - 1, self.tension_v + 1)
        plt.ylabel(t['labels'])
        plt.title(t['title'])

        # Añadir anotación del porcentaje
        plt.text(1, tensiones[1] + 0.2, t['annotations'], ha='center', fontweight='bold')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()


# %% [DEMOSTRACIÓN]
if __name__ == "__main__":
    # Creamos un escenario válido (C1 estándar)
    # Ib = ~0.87A, In = 10A, Iz = 15.22A (según tu PDF)
    circuito_ok = CircuitoResidencialREBT(
        nombre="C1 - Alumbrado OK",
        tension_v=230,
        longitud_m=10,
        seccion_mm2=1.5,
        potencia_w=200,
        tipo_uso='alumbrado',
        i_n=10,
        i_z=15.22,
        lang='ES'
    )
    circuito_ok.imprimir_informe()

    # Creamos un escenario que FALLARÁ (La caída del 9% que viste)
    # Simulamos 60 metros de cable con 3500W en un cable de 1.5mm2
    circuito_fallo = CircuitoResidencialREBT(
        nombre="C1 - Alumbrado LARGO (Fallo)",
        tension_v=230,
        longitud_m=60,  # Longitud excesiva
        seccion_mm2=1.5,
        potencia_w=3500,  # Potencia excesiva
        tipo_uso='alumbrado',
        i_n=10,
        i_z=15.22,
        lang='ES'
    )
    circuito_fallo.imprimir_informe()
    circuito_fallo.plot_resultados()