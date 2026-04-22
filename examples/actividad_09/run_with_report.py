# %% [markdown]
# # Reporte de Centralización de Contadores (CC)
# Automated evaluation and layout generation for ITC-BT-16 compliance.
import os
print(os.getcwd())
# %%
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Language toggle switch
LANG = 'ES'

# Presentation dictionary for bilingual plotting
plot_meta = {
    "EN": {
        "fig_title": "Meter Centralization: Layout Proposals",
        "case": "Case",
        "type_room": "ROOM (Local)",
        "type_closet": "CLOSET (Armario)",
        "clearance": "Clearance",
        "wall": "Wall",
        "door": "Door (PF60)",
        "unit": "Meter Units"
    },
    "ES": {
        "fig_title": "Centralización de Contadores: Croquis de Propuestas",
        "case": "Caso",
        "type_room": "LOCAL",
        "type_closet": "ARMARIO",
        "clearance": "Espacio Libre",
        "wall": "Pared",
        "door": "Puerta (PF60)",
        "unit": "Unidades de Medida"
    }
}

txt = plot_meta[LANG]


# %% THE RULES ENGINE (Decoupled Logic)
class RuleNode:
    def __init__(self, name, predicate, on_true, on_false):
        self.name = name
        self.predicate = predicate
        self.on_true = on_true
        self.on_false = on_false

    def evaluate(self, context):
        result = self.predicate(context)
        next_step = self.on_true if result else self.on_false
        if isinstance(next_step, RuleNode):
            return next_step.evaluate(context)
        return next_step


# Independent Nodes
igm_node = RuleNode("Load>=90", lambda c: c['load_kw'] >= 90, "250A", "160A")
type_node = RuleNode("Meters>16", lambda c: c['total_meters'] > 16, "Local", "Armario")

# %% 2. CASE DATA PROCESSING
cases = [
    {"id": "01", "load_kw": 92.37, "total_meters": 17},
    {"id": "02", "load_kw": 75.0, "total_meters": 9},
    {"id": "03", "load_kw": 145.15, "total_meters": 23}
]

# Run the engine
results = []
for c in cases:
    results.append({
        "id": c["id"],
        "type": type_node.evaluate(c),
        "igm": igm_node.evaluate(c),
        "meters": c["total_meters"]
    })

# %% PRESENTATION LAYER (Plotting for PDF Export)

fig, axes = plt.subplots(3, 1, figsize=(5, 15))
fig.suptitle(txt["fig_title"], fontsize=16, fontweight='bold', y=1.05)

for i, res in enumerate(results):
    ax = axes[i]
    ax.set_aspect('equal')
    ax.axis('off')

    # Title showing Engine Output
    ax.set_title(f"{txt['case']} {res['id']}\n{res['type']} | IGM: {res['igm']}",
        fontsize=12, pad=10)

    # Draw parameters based on logic result
    if res['type'] == "Armario":
        # Draw Wall
        ax.plot([-50, 250], [0, 0], color='black', linewidth=3, label=txt['wall'])
        # Draw Armario
        armario = patches.Rectangle((0, 0), 200, 40, edgecolor='blue', facecolor='lightblue')
        ax.add_patch(armario)
        ax.text(100, 20, txt['type_closet'], ha='center', va='center', fontsize=10)
        # Draw Clearance (150 cm)
        clearance = patches.Rectangle((0, -150), 200, 150, edgecolor='red', linestyle='--', fill=False)
        ax.add_patch(clearance)
        ax.text(100, -75, f"150 cm\n{txt['clearance']}", ha='center', va='center', color='red')

        ax.set_xlim(-50, 250)
        ax.set_ylim(-200, 100)

    else:
        # Draw Local Room (Min width 150cm, typically larger for >16 meters)
        room_width = 250
        room_depth = 200
        # Walls
        ax.plot([0, room_width], [room_depth, room_depth], color='black', linewidth=3)  # Top
        ax.plot([0, 0], [0, room_depth], color='black', linewidth=3)  # Left
        ax.plot([room_width, room_width], [0, room_depth], color='black', linewidth=3)  # Right
        ax.plot([70, room_width], [0, 0], color='black', linewidth=3)  # Bottom (with 70cm door)

        # Door
        ax.plot([0, 70], [0, 70], color='gray', linestyle=':')
        ax.text(10, 35, txt['door'], rotation=45, fontsize=8, color='gray')

        # Meter Units mounted on top wall
        units = patches.Rectangle((20, room_depth - 40), room_width - 40, 40, edgecolor='blue', facecolor='lightblue')
        ax.add_patch(units)
        ax.text(room_width / 2, room_depth - 20, txt['unit'], ha='center', va='center', fontsize=10)

        # Draw Clearance (110 cm)
        clearance = patches.Rectangle((20, room_depth - 150), room_width - 40, 110, edgecolor='red', linestyle='--',
            fill=False)
        ax.add_patch(clearance)
        ax.text(room_width / 2, room_depth - 95, f"110 cm\n{txt['clearance']}", ha='center', va='center', color='red')

        ax.set_xlim(-50, 300)
        ax.set_ylim(-50, 250)

plt.tight_layout()
# Uncomment the line below to save directly to PDF in your environment
plt.savefig("actividad_09_croquis.pdf", format="pdf", bbox_inches="tight")
plt.show()