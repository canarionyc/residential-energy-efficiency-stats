# REBT ITC-BT-25: [Amps, Section_mm2, Tube_mm, Max_Points]
REBT_CATALOG = {
    "C1": [10, 1.5, 16, 30],
    "C2": [16, 2.5, 20, 20],
    "C3": [25, 6.0, 25, 2],
    "C4": [20, 4.0, 20, 3],
    "C5": [16, 2.5, 20, 6],
    "C8": [10, 1.5, 16, 99], # Domotics
    "C10": [16, 2.5, 20, 1]  # Dryer
}
STANDARD_SECTIONS = [1.5, 2.5, 4.0, 6.0, 10.0, 16.0]
TUBE_DIAMETERS = {1.5: 16, 2.5: 20, 4.0: 20, 6.0: 25, 10.0: 25, 16.0: 32}

LANG = "ES"
labels_config = {
    "EN": {
        "panel": "PANEL",
        "iga": "IGA (Main Switch)",
        "rcd": "RCD",
        "wire": "Wire",
        "tube": "Tube",
        "pts": "pts",
        "len": "L="
    },
    "ES": {
        "panel": "CUADRO",
        "iga": "IGA (Interruptor General)",
        "rcd": "ID (Diferencial)",
        "wire": "Cond.",
        "tube": "Tubo",
        "pts": "pts",
        "len": "L="
    }
}
labels = labels_config[LANG]