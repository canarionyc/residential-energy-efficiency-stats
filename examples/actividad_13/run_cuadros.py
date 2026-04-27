#%% BILINGUAL CONFIGURATION & BASELINES
import math

from panel import Panel
from rcd_group import RCDGroup
from circuit import Circuit

from constants import LANG





#%% CIRCUIT AND PANEL CLASSES




# class Panel:
#     def __init__(self, name, power_w=None):
#         self.name = name
#         self.power_w = power_w
#         self.iga_amps = self._estimate_iga()
#         self.rcd_groups = []
#
#
#     def add_rcd(self, rcd_group):
#         self.rcd_groups.append(rcd_group)
#



# %% CASO PRÁCTICO 01
# Realizar el esquema unifilar del cuadro de distribución, protección y mando de una
# vivienda, en la que no se sabe la potencia contratada por el usuario y donde se han
# desdoblado los circuitos C2 y C5, por cuestiones de diseño. El circuito C4 se desdobla en
# tres, y se prevé un circuito de domótica. El número de puntos de luz a instalar en la
# vivienda es de 45 puntos. Se deberá indicar el número máximo de puntos en cada circuito,
# así como las secciones mínimas de los conductores y el diámetro de los tubos de
# protección. El alumno debe estimar el ICP posible a instalar.
def run_case_1():
    # Caso 1: Potencia desconocida, C2/C5 desdoblados, C4 en 3, Domótica[cite: 2, 3].
    p = Panel("CASO PRÁCTICO 01 (Potencia Desconocida)")
    
    r1 = RCDGroup("1")
    r1.add(Circuit("C1", "Iluminación", points=45)) # C1 not explicitly split, triggers warning 
    r1.add(Circuit("C2", "Uso general 1", points=10))
    r1.add(Circuit("C2", "Uso general 2", points=10))
    r1.add(Circuit("C8", "Domótica", points=1))
    
    r2 = RCDGroup("2")
    r2.add(Circuit("C3", "Cocina/Horno", points=2))
    r2.add(Circuit("C4", "Lavadora", points=1))
    r2.add(Circuit("C4", "Lavavajillas", points=1))
    r2.add(Circuit("C4", "Termo", points=1))
    r2.add(Circuit("C5", "Baño", points=3))
    r2.add(Circuit("C5", "Cocina tomas", points=3)) # Exceeds 5 circuits per RCD intentionally to show needed fix
    
    p.add_rcd(r1)
    p.add_rcd(r2)
    p.render()

    p.generate_audit_report()

# %% CASO PRÁCTICO 02
# Realizar el esquema unifilar del cuadro de distribución, protección y mando de una
# vivienda, en la que la potencia contratada y la previsión de carga es 9.200W y los circuitos
# tienen las siguientes restricciones:
# C1: Iluminación. 46 puntos. Longitud 27 m.
# C2: Uso general. 30 puntos. Longitud 30 m.
# C3: Cocina y horno. 2 puntos. Longitud 10 m.
# C4: Lavadora, Lavavajillas, termo. 3 puntos. Longitud 18 m.
# C5: Baño, cuarto de cocina. 8 tomas. Longitud 15 m.
# C10: Secadora. 1 toma. Longitud 18 m.
# SE PIDE:
# Esquema Unifilar del CDMP indicando:
# a) ICP
# b) IGA
# c) Sf, Sn, Sp
# d) Diámetro del tubo
# e) Protecciones magnetotérmicas y diferenciales empleadas.
def run_case_2():
    # Caso 2: 9.200W, specific lengths restricting physics[cite: 6].
    p = Panel("CASO PRÁCTICO 02 (9.200W)", power_w=9200)
    
    r1 = RCDGroup("1")
    r1.add(Circuit("C1", "Iluminación", points=46, length_m=27))
    r1.add(Circuit("C4", "Lav/Lavav/Termo", points=3, length_m=18))
    r1.add(Circuit("C5", "Baño/Cocina", points=8, length_m=15))
    r2 = RCDGroup("2")
    r2.add(Circuit("C2", "Uso general", points=30, length_m=30))
    r2.add(Circuit("C3", "Cocina y horno", points=2, length_m=10))
    r2.add(Circuit("C10", "Secadora", points=1, length_m=18))
    
    p.add_rcd(r1)
    p.add_rcd(r2)
    p.render()

    p.generate_audit_report()

# %% CASO PRÁCTICO 03
# Realizar el esquema unifilar del cuadro de distribución, protección y mando de una
# vivienda, en la que no se sabe la potencia contratada por el usuario y donde se han
# desdoblado los circuitos C1, C2, y C5. El circuito C4 se desdobla en tres, y se prevé un
# circuito de domótica. Se deberá indicar el número máximo de puntos en cada circuito, así
# como las secciones mínimas de los conductores y el diámetro de los tubos de protección.
def run_case_3():
    # Caso 3: Potencia desconocida, C1/C2/C5 desdoblados, C4 en 3, Domótica[cite: 11, 12].
    p = Panel("CASO PRÁCTICO 03 (Potencia Desconocida - Elevada)")
    
    r1 = RCDGroup("1")
    r1.add(Circuit("C1", "Iluminación 1", points=15))
    r1.add(Circuit("C2", "Uso general 1", points=10))
    r1.add(Circuit("C5", "Baño", points=3))
    r1.add(Circuit("C4", "Lavadora", points=1))
    r1.add(Circuit("C8", "Domótica", points=1))
    
    r2 = RCDGroup("2")
    r2.add(Circuit("C1", "Iluminación 2", points=15))
    r2.add(Circuit("C2", "Uso general 2", points=10))
    r2.add(Circuit("C5", "Cocina tomas", points=3))
    r2.add(Circuit("C4", "Lavavajillas", points=1))
    r2.add(Circuit("C3", "Cocina/Horno", points=2))
    
    r3 = RCDGroup("3")
    r3.add(Circuit("C4", "Termo", points=1))
    
    p.add_rcd(r1)
    p.add_rcd(r2)
    p.add_rcd(r3)

    p.generate_audit_report()

    p.render()

# %% CASO PRÁCTICO 04
# Realizar el esquema unifilar del cuadro de distribución, protección y mando de una
# vivienda, en la que la potencia contratada es 5.750 W y la distribución de los circuitos se
# ha de realizar según el siguiente diseño:
# Zona de garaje:
# C1: Iluminación. 4 puntos.
# C2: Uso general. 6 puntos.
# Planta Baja:
# C1: Iluminación. 33 puntos.
# C2: Uso general. 16 puntos.
# C3: Cocina y horno. 1 punto.
# C5: Baño, cuarto de cocina. 8 tomas.
# C10: Secadora. 1 toma.
# Planta Alta:
# C1: Iluminación. 25 puntos.
# C2: Uso general. 14 puntos.
# C5: Baño, cuarto de cocina. 3 tomas.
# Buhardilla:
# 1 Dormitorio
# 1 Baño
# SE PIDE:
# Esquema Unifilar del CDMP indicando:
# a) ICP
# b) IGA
# c) Sf, Sn, Sp
# d) Diámetro del tubo
# e) Protecciones magnetotérmicas y diferenciales empleadas


def run_case_4():
    # Inicializamos el panel.
    # NOTA TÉCNICA: 5750W genera un IGA de 25A. En una obra real,
    # la presencia de C10 y los desdoblamientos C1/C5 invalidarían el
    # boletín para 5750W, requiriendo saltar a 9200W (IGA 40A).
    p = Panel("CASO PRÁCTICO 04 (Contrato 5.750W / Topología Elevada)", power_w=5750)

    # ID 1: Planta Baja (Zona A) - Agrupando cargas pesadas y alumbrado dividido
    r1 = RCDGroup("1 (Planta Baja A)")
    r1.add(Circuit("C1", "Iluminación PB (A)", points=17))  # Desdoblado de los 33 originales
    r1.add(Circuit("C2", "Uso general PB", points=16))
    r1.add(Circuit("C3", "Cocina y horno", points=1))
    r1.add(Circuit("C5", "Baño/Cocina PB (A)", points=4))  # Desdoblado de los 8 originales
    r1.add(Circuit("C10", "Secadora", points=1))

    # ID 2: Planta Baja (Zona B) y Planta Alta
    r2 = RCDGroup("2 (Planta Baja B + Planta Alta)")
    r2.add(Circuit("C1", "Iluminación PB (B)", points=16))  # El resto del alumbrado de PB
    r2.add(Circuit("C1", "Iluminación PA", points=25))
    r2.add(Circuit("C2", "Uso general PA", points=14))
    r2.add(Circuit("C5", "Baño/Cocina PB (B)", points=4))  # El resto de cuartos húmedos PB
    r2.add(Circuit("C5", "Baños PA", points=3))

    # ID 3: Garaje y Buhardilla
    # Dotación mínima de la buhardilla (1 Dormitorio, 1 Baño) añadida normativamente
    r3 = RCDGroup("3 (Garaje + Buhardilla)")
    r3.add(Circuit("C1", "Iluminación Garaje", points=4))
    r3.add(Circuit("C2", "Uso general Garaje", points=6))
    r3.add(Circuit("C1", "Iluminación Buhardilla", points=2))  # Luz cuarto y baño
    r3.add(Circuit("C2", "Uso gen. Dormitorio Buh.", points=3))  # Enchufes dormitorio
    r3.add(Circuit("C5", "Baño Buhardilla", points=1))  # Enchufe baño

    p.add_rcd(r1)
    p.add_rcd(r2)
    p.add_rcd(r3)

    p.generate_audit_report()

    p.render()

# %% EXE
if __name__ == "__main__":
    # run_case_1()
    # run_case_2()
    # run_case_3()
    run_case_4()