

# ACTIVIDAD 13: ESQUEMAS UNIFILARES (CDMP)

## CASO PRÁCTICO 01: Electrificación Elevada (Potencia Desconocida)

**Descripción del Diseño:**
* Se han instalado 45 puntos de iluminación (requiere desdoblamiento de C1).
* Circuitos C2 y C5 desdoblados por diseño.
* Circuito C4 desdoblado en tres ramas independientes.
* Previsión de circuito de domótica (C11).
* Al cumplir criterios de electrificación elevada, el IGA se establece en 40A (9.200W).

### Esquema Unifilar (Caso 01)
```text
[CUADRO GENERAL DE MANDO Y PROTECCIÓN]
|-- [IGA] 40A
       |
       +-- [ID 1] 40A / 30mA
                |-- C1a - Iluminación (Zona A): PIA 10A | 1.5mm² | Tubo 16mm | 23 pts 
                |-- C2a - Uso general 1: PIA 16A | 2.5mm² | Tubo 20mm | 10 pts 
                |-- C3 - Cocina/Horno: PIA 25A | 6.0mm² | Tubo 25mm | 2 pts 
                +-- C11 - Domótica: PIA 10A | 1.5mm² | Tubo 16mm | 1 pts 
       |
       +-- [ID 2] 40A / 30mA
                |-- C1b - Iluminación (Zona B): PIA 10A | 1.5mm² | Tubo 16mm | 22 pts 
                |-- C2b - Uso general 2: PIA 16A | 2.5mm² | Tubo 20mm | 10 pts 
                |-- C4a - Lavadora: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
                |-- C4b - Lavavajillas: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
                |-- C4c - Termo eléctrico: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
                |-- C5a - Baño: PIA 16A | 2.5mm² | Tubo 20mm | 3 pts 
                +-- C5b - Cocina (tomas): PIA 16A | 2.5mm² | Tubo 20mm | 3 pts 
```

### Informe de Auditoría (Caso 01)
| Tipo | Puntos Totales | Núm. PIAs | Uso Típico |
| :--- | :---: | :---: | :--- |
| C1 | 45 | 2 | Iluminación [cite: 104-106] |
| C2 | 20 | 2 | Tomas de uso general  |
| C3 | 2 | 1 | Cocina y Horno  |
| C4 | 3 | 3 | Lavadora, Lavavajillas, Termo  |
| C5 | 6 | 2 | Baños y auxiliares de cocina  |
| C11 | 1 | 1 | Domótica  |

* **Total PIAs Físicos:** 11.
* **Grado de Electrificación:** Elevada.

---

## CASO PRÁCTICO 02: Previsión de Carga 9.200 W

**Restricciones de Diseño:**
* Longitudes elevadas en C1 (27m) y C2 (30m) que obligan a verificar caída de tensión[cite: 14, 15, 115, 116].
* 46 puntos de luz (desdoblamiento obligatorio de C1).
* Circuito C10 para secadora incluido.

### Esquema Unifilar (Caso 02)
```text
[CUADRO GENERAL DE MANDO Y PROTECCIÓN]
|-- [IGA] 40A
       |
       +-- [ID 1] 40A / 30mA
                |-- C1a - Iluminación (27m): PIA 10A | 2.5mm² | Tubo 20mm | 23 pts 
                |-- C2a - Uso general (30m): PIA 16A | 2.5mm² | Tubo 20mm | 15 pts 
                |-- C4 - Lav/Lavav/Termo: PIA 20A | 4.0mm² | Tubo 20mm | 3 pts 
                +-- C5a - Baño/Cocina: PIA 16A | 2.5mm² | Tubo 20mm | 4 pts 
       |
       +-- [ID 2] 40A / 30mA
                |-- C1b - Iluminación (27m): PIA 10A | 2.5mm² | Tubo 20mm | 23 pts 
                |-- C2b - Uso general (30m): PIA 16A | 2.5mm² | Tubo 20mm | 15 pts 
                |-- C3 - Cocina y horno: PIA 25A | 6.0mm² | Tubo 25mm | 2 pts 
                |-- C5b - Baño/Cocina: PIA 16A | 2.5mm² | Tubo 20mm | 4 pts 
                +-- C10 - Secadora: PIA 16A | 2.5mm² | Tubo 20mm | 1 pts 
```

### Informe de Auditoría (Caso 02)
| Tipo | Puntos Totales | Núm. PIAs | Uso Típico |
| :--- | :---: | :---: | :--- |
| C1 | 46 | 2 | Iluminación [cite: 125-127] |
| C2 | 30 | 2 | Uso general  |
| C3 | 2 | 1 | Cocina y horno  |
| C4 | 3 | 1 | Lavadora, Lavavajillas, Termo  |
| C5 | 8 | 2 | Baño y Cocina  |
| C10 | 1 | 1 | Secadora  |

* **Potencia de Diseño:** 9.200 W.
* **Total PIAs Físicos:** 9.

---

## CASO PRÁCTICO 03: Potencia Desconocida (Desdoblamiento Máximo)

**Descripción del Diseño:**
* Desdoblamiento de circuitos C1, C2 y C5 por requerimiento.
* El circuito C4 se divide en tres ramas independientes.
* Inclusión de domótica (C11).

### Esquema Unifilar (Caso 03)
```text
[CUADRO GENERAL DE MANDO Y PROTECCIÓN]
|-- [IGA] 40A
       |
       +-- [ID 1] 40A / 30mA
                |-- C1a - Iluminación 1: PIA 10A | 1.5mm² | Tubo 16mm | 15 pts 
                |-- C2a - Uso general 1: PIA 16A | 2.5mm² | Tubo 20mm | 10 pts 
                |-- C5a - Baño: PIA 16A | 2.5mm² | Tubo 20mm | 3 pts 
                |-- C4a - Lavadora: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
                +-- C11 - Domótica: PIA 10A | 1.5mm² | Tubo 16mm | 1 pts 
       |
       +-- [ID 2] 40A / 30mA
                |-- C1b - Iluminación 2: PIA 10A | 1.5mm² | Tubo 16mm | 15 pts 
                |-- C2b - Uso general 2: PIA 16A | 2.5mm² | Tubo 20mm | 10 pts 
                |-- C4b - Lavavajillas: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
                |-- C5b - Cocina (tomas): PIA 16A | 2.5mm² | Tubo 20mm | 3 pts 
                +-- C3 - Cocina/Horno: PIA 25A | 6.0mm² | Tubo 25mm | 2 pts 
       |
       +-- [ID 3] 40A / 30mA
                +-- C4c - Termo eléctrico: PIA 20A | 4.0mm² | Tubo 20mm | 1 pts 
```

### Informe de Auditoría (Caso 03)
| Tipo | Puntos Totales | Núm. PIAs | Uso Típico |
| :--- | :---: | :---: | :--- |
| C1 | 30 | 2 | Iluminación [cite: 150-152] |
| C2 | 20 | 2 | Uso general  |
| C3 | 2 | 1 | Cocina y Horno  |
| C4 | 3 | 3 | Lavadora, Lavavajillas, Termo  |
| C5 | 6 | 2 | Baños y Cocina  |
| C11 | 1 | 1 | Domótica  |

* **Total PIAs Físicos:** 11.

---

## CASO PRÁCTICO 04: Contrato 5.750 W (Distribución por Zonas)

**Distribución Espacial:**
* Incluye zonas de Garaje, Planta Baja, Planta Alta y Buhardilla[cite: 36, 39, 45, 49].
* Aunque el contrato es de 5.750W, la topología es de Electrificación Elevada debido a la secadora y los desdoblamientos necesarios.

### Esquema Unifilar (Caso 04)
```text
[CUADRO GENERAL DE MANDO Y PROTECCIÓN]
|-- [IGA] 40A (Soportando topología elevada) 
       |
       +-- [ID 1 - Planta Baja A] 40A / 30mA
                |-- C1 - Iluminación PB (A): PIA 10A | 1.5mm² | 16mm | 17 pts 
                |-- C2 - Uso general PB: PIA 16A | 2.5mm² | 20mm | 16 pts 
                |-- C3 - Cocina y horno: PIA 25A | 6.0mm² | 25mm | 1 pts 
                |-- C5 - Baño/Cocina PB (A): PIA 16A | 2.5mm² | 20mm | 4 pts 
                +-- C10 - Secadora: PIA 16A | 2.5mm² | 20mm | 1 pts 
       |
       +-- [ID 2 - Planta Baja B + Planta Alta] 40A / 30mA
                |-- C1 - Iluminación PB (B): PIA 10A | 1.5mm² | 16mm | 16 pts 
                |-- C1 - Iluminación PA: PIA 10A | 1.5mm² | 16mm | 25 pts 
                |-- C2 - Uso general PA: PIA 16A | 2.5mm² | 20mm | 14 pts 
                |-- C5 - Baño/Cocina PB (B): PIA 16A | 2.5mm² | 20mm | 4 pts 
                +-- C5 - Baños PA: PIA 16A | 2.5mm² | 20mm | 3 pts 
       |
       +-- [ID 3 - Garaje + Buhardilla] 40A / 30mA
                |-- C1 - Iluminación Garaje: PIA 10A | 1.5mm² | 16mm | 4 pts 
                |-- C2 - Uso general Garaje: PIA 16A | 2.5mm² | 20mm | 6 pts 
                |-- C1 - Iluminación Buhardilla: PIA 10A | 1.5mm² | 16mm | 2 pts 
                |-- C2 - Uso gen. Dormitorio Buh.: PIA 16A | 2.5mm² | 20mm | 3 pts [cite: 175-177]
                +-- C5 - Baño Buhardilla: PIA 16A | 2.5mm² | 20mm | 1 pts 
```

### Informe de Auditoría (Caso 04)
| Tipo | Puntos Totales | Núm. PIAs | Uso Típico |
| :--- | :---: | :---: | :--- |
| C1 | 64 | 5 | Iluminación General [cite: 179-181] |
| C2 | 39 | 4 | Uso general  |
| C3 | 1 | 1 | Cocina y horno  |
| C5 | 12 | 4 | Zonas húmedas  |
| C10 | 1 | 1 | Secadora  |

* **Potencia de Diseño:** 5.750 W (Contratada).
* **Total PIAs Físicos:** 15.