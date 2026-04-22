#%% setup
from examples.actividad_09.nodeRepository import location_node, type_node, igm_node

#%% Data extracted from ACTIVIDAD_09_CC_enunciado.pdf
cases = [
    {"id": "CASE 01", "floors": 4, "load_kw": 92.37, "total_meters": 17},
    {"id": "CASE 02", "floors": 4, "load_kw": 75.0, "total_meters": 9},
    {"id": "CASE 03", "floors": 9, "load_kw": 145.15, "total_meters": 23}
]

for case in cases:
    print(f"--- Results for {case['id']} ---")

    # We run each independent rule-set
    # In a more complex DAG, these would be branches of a single root node
    for logic_chain in [location_node, type_node, igm_node]:
        output = logic_chain.run(case)
        print(f"DECISION: {output['result']}")
        for msg in output['messages']:
            print(f"  [Log] {msg}")
    print("\n")