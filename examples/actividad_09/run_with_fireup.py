# %% [markdown]
# # Centralización de Contadores - Certified Engine
# 1. Startup Primer: Validates the Rulebook structure.
# 2. Execution: Minimalist data-trace for case accountability.
import pprint
from examples.actividad_09.rulebook import RuleEngine, RuleNode
from examples.actividad_09.nodeRepository import type_node, igm_node

# %% Building and Priming the Engine
engine_type = RuleEngine(type_node)
engine_igm = RuleEngine(igm_node)

engine_type.fireup_test()
engine_igm.fireup_test()

# %% Data from Activity 09
# Test Case 03: 23 meters (should trigger Local cascade)
case_03 = {
    "meters_monophase": 16,
    "meters_threephase": 6 + 1,  # 6 Locales + 1 Serv. Generales
    "total_meters": 23,
    "room_height": 2.40,
    "frontal_clearance": 1.20
}

cases = [
    {"id": "CASE 01", "load_kw": 92.37,
        "meters_monophase": 9,
        "meters_threephase": 7 + 1,  # 7 Locales + 1 Serv. Generales
        "total_meters": 17},
    {"id": "CASE 02", "load_kw": 75.0,
        "meters_monophase": 6,
        "meters_threephase": 2 + 1,  # 2 Locales + 1 Serv. Generales
        "total_meters": 9},
    {"id": "CASE 03", "load_kw": 145.15, **case_03}
]
from pprint import pprint

pprint(cases)

# %% run cases
for case in cases:
    print(f"--- RESULTADOS {case['id']} ---")
    print(f"Datos de entrada: Carga={case['load_kw']}kW, Contadores={case['total_meters']}")
    res_type = engine_type.run(case)
    res_igm = engine_igm.run(case)

    print(f"DECISIÓN: {res_type['result']} | {res_igm['result']}")
    print("TRAZA DE DATOS:")
    for entry in res_type['history'] + res_igm['history']:
        print(f"  [Dato] {entry}")
    print("-" * 30)
# %%