import json
from examples.actividad_09.rulebook import RuleNode
# Node for IGM rating based on electrical load
# igm_node = RuleNode(
#     name="IGM Rating",
#     predicate=lambda c: c['load_kw'] < 90,
#     on_false="IGM: 250A",
#     on_true="IGM: 160A"
# )




# %% Define independent nodes (The 'Machine' parts)
igm_node = RuleNode("¿Carga < 90kW?", lambda c: c['load_kw'] < 90, "IGM: 160A", "IGM: 250A")
type_node = RuleNode("¿Contadores > 16?", lambda c: c['total_meters'] > 16, "Tipo: Local", "Tipo: Armario")


# # Node for installation type based on number of meters
# type_node = RuleNode(
#     name="Installation Type",
#     predicate=lambda c: c['total_meters'] <= 16,
#     on_false="Type: Local (Room)",
#     on_true="Type: Armario (Closet)"
# )

# Root node: Evaluating location (assuming buildings < 12 floors for this activity)
location_node = RuleNode(
    name="Location Check",
    predicate=lambda c: c['floors'] <= 12,
    on_true="Location: Ground Floor (Planta Baja)",
    on_false="Location: Distributed (Every 6 floors)"
)

# Requirements for a Local (Room)
local_requirements = RuleNode(
    "Local Dimension Check (Height >= 2.30m)",
    lambda c: c.get('room_height', 0) >= 2.30,
    on_true="COMPLIANT: Local with PF60 door and 1.10m clearance.",
    on_false="NON-COMPLIANT: Local height insufficient."
)

# Requirements for an Armario (Closet)
armario_requirements = RuleNode(
    "Armario Clearance Check (Frontal >= 1.50m)",
    lambda c: c.get('frontal_clearance', 0) >= 1.50,
    on_true="COMPLIANT: Armario with PF30 door.",
    on_false="NON-COMPLIANT: Insufficient frontal space."
)

# --- MAIN LOGIC ROOT ---

# root_node = RuleNode(
#     "Installation Type (Meters > 16)",
#     lambda c: c['total_meters'] > 16,
#     on_true=local_requirements,  # CASCADES to local rules
#     on_false=armario_requirements  # CASCADES to armario rules
# )