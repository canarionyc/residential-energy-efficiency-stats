# %% markdown
# # Actividad 12: Derivación Individual (DI)
# Sizing and constructive details for Individual Derivations.

# %% cases
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

LANG = 'ES'

# The Data State from the assignment
cases = {
    "CASE_01": {
        "electrification": "Elevado",
        "system": "B1", # Conducto de obra de fábrica
        "length_m": 12,
        "power_w": 5750,
        "temp_c": 30,
        "num_di": 9
    },
    "CASE_02": {
        "electrification": "Básico",
        "system": "B1",
        "length_m": 35,
        "power_w": 5750,
        "temp_c": 40, # Note the higher temperature
        "num_di": 1 # Implicit, just sizing for one unless specified
    },
    "CASE_03": {
        "electrification": "Elevado",
        "system": "A1", # Note the different installation system
        "length_m": 40,
        "power_w": 9200,
        "temp_c": 30,
        "num_di": 16
    }
}