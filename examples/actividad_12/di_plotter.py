#%% setup
import os
from pathlib import Path
# current_folder = Path(__file__).parent
# here = lambda x: Path(__file__).parent / x
# print(here("."))

# current_folder = os.getcwd()

# If you are running this inside a Jupyter Notebook instead of a standard .py script, __file__ is not defined. In
# Jupyter, Path.cwd() is used to get the current working directory of the notebook
# current_folder = Path.cwd()

# from pyprojroot import here
# project_root = here()
#
#
# print(f"current_folder: {project_root}")
#
# print(here("pdf/actividad_12"))

output_dir=Path.cwd() / "pdf/actividad_12"
output_dir.mkdir(parents=True, exist_ok=True)
print(f"output_dir: {output_dir}")

# %% Presentation Dictionary
plot_meta = {
    "EN": {
        "title": "Constructive Detail: Factory Conduit",
        "shaft": "Brick Shaft",
        "tube": "DI Tube",
        "cover": "Fire-resistant Cover"
    },
    "ES": {
        "title": "Detalle Constructivo: Conducto de Obra de Fábrica",
        "shaft": "Mocheta / Obra de Fábrica",
        "tube": "Tubo DI",
        "cover": "Tapa Registro (RF)"
    }
}


def plot_conduit_detail(num_tubes, tube_diameter_mm, case_id):
    """
    Plots the cross-section of the masonry conduit.
    """
    txt = plot_meta[LANG]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title(f"{txt['title']} - {case_id}\n({num_tubes} {txt['tube']}s)", fontsize=14, pad=20)

    # Calculate grid for tubes
    cols = math.ceil(math.sqrt(num_tubes))
    rows = math.ceil(num_tubes / cols)

    spacing = tube_diameter_mm * 1.5
    shaft_width = cols * spacing + spacing
    shaft_height = rows * spacing + spacing

    # Draw Brick Shaft (U-shape)
    shaft = patches.Rectangle((0, 0), shaft_width, shaft_height,
        linewidth=4, edgecolor='brown', facecolor='none', hatch='//')
    ax.add_patch(shaft)

    # Draw Cover (Frontal)
    cover = patches.Rectangle((0, -10), shaft_width, 10,
        linewidth=2, edgecolor='black', facecolor='lightgray')
    ax.add_patch(cover)

    # Draw Tubes
    for r in range(rows):
        for c in range(cols):
            if r * cols + c < num_tubes:
                cx = spacing + c * spacing
                cy = spacing + r * spacing
                tube = patches.Circle((cx, cy), tube_diameter_mm / 2,
                    linewidth=2, edgecolor='black', facecolor='white')
                ax.add_patch(tube)

                # Draw 3 small circles inside to represent Phase, Neutral, Earth
                ax.add_patch(patches.Circle((cx - 3, cy + 3), 2, facecolor='black'))  # Phase
                ax.add_patch(patches.Circle((cx + 3, cy + 3), 2, facecolor='blue'))  # Neutral
                ax.add_patch(patches.Circle((cx, cy - 4), 2, facecolor='green'))  # Earth

    ax.set_xlim(-20, shaft_width + 20)
    ax.set_ylim(-30, shaft_height + 20)

    # Save to PDF
    plt.tight_layout()
    plt.savefig(output_dir/ f"{case_id}_detalle_constructivo.pdf", format="pdf", bbox_inches="tight")
    # plt.show()