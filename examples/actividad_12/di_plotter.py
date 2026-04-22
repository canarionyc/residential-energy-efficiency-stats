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
        "cover": "Fire-resistant Cover",
        "case_label": "Case Data",
        "results_label": "Calculation Results",
        "electrification": "Electrification",
        "system": "System",
        "length": "Length (m)",
        "power": "Power (W)",
        "temp": "Temp. (°C)",
        "num_di": "No. of DIs",
        "s_thermal": "Thermal limit (mm²)",
        "s_voltage": "Voltage drop (mm²)",
        "s_regulatory": "Regulatory min. (mm²)",
        "final_section": "▶ Final section (mm²)",
    },
    "ES": {
        "title": "Detalle Constructivo: Conducto de Obra de Fábrica",
        "shaft": "Mocheta / Obra de Fábrica",
        "tube": "Tubo DI",
        "cover": "Tapa Registro (RF)",
        "case_label": "Datos del Caso",
        "results_label": "Resultados del Cálculo",
        "electrification": "Electrificación",
        "system": "Sistema",
        "length": "Longitud (m)",
        "power": "Potencia (W)",
        "temp": "Temp. (°C)",
        "num_di": "Nº DIs",
        "s_thermal": "Límite térmico (mm²)",
        "s_voltage": "Caída de tensión (mm²)",
        "s_regulatory": "Mínimo normativo (mm²)",
        "final_section": "▶ Sección final (mm²)",
    }
}


def _build_case_text(txt, case_data):
    lines = [txt["case_label"], "─" * 22]
    lines.append(f"{txt['electrification']}: {case_data.get('electrification', '—')}")
    lines.append(f"{txt['system']}: {case_data.get('system', '—')}")
    lines.append(f"{txt['length']}: {case_data.get('length_m', '—')}")
    lines.append(f"{txt['power']}: {case_data.get('power_w', '—')}")
    lines.append(f"{txt['temp']}: {case_data.get('temp_c', '—')}")
    lines.append(f"{txt['num_di']}: {case_data.get('num_di', '—')}")
    return "\n".join(lines)


def _build_results_text(txt, results):
    lines = [txt["results_label"], "─" * 22]
    lines.append(f"{txt['s_thermal']}: {results.get('s_thermal', '—')}")
    lines.append(f"{txt['s_voltage']}: {results.get('s_voltage', '—')}")
    lines.append(f"{txt['s_regulatory']}: {results.get('s_regulatory', '—')}")
    lines.append(f"{txt['final_section']}: {results.get('final_commercial_section', '—')}")
    return "\n".join(lines)


def plot_conduit_detail( case_data, results):
    """
    Plots the cross-section of the masonry conduit.
    Renders a case data panel (left) and results panel (right).

    Args:
        num_tubes (int): The number of Individual Derivations to draw.
        case_data (dict): The input parameters for the case.
        results (dict): The output calculations from the solver.
    """
    txt = plot_meta[LANG]

    # Extract variables that used to be passed as arguments
    num_tubes = case_data["num_di"]
    case_id = case_data.get("id", "Unknown_Case")
    tube_diameter_mm = results.get("tube_diameter_mm", 32)  # Fallback to 32mm if not present

    # Since case_data and results are now compulsory, we always draw the 3-panel layout
    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 2, 1], wspace=0.05)

    ax_left = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])
    ax_right = fig.add_subplot(gs[2])

    for side_ax in (ax_left, ax_right):
        side_ax.axis('off')

    ax_left.text(0.05, 0.95, _build_case_text(txt, case_data),
        transform=ax_left.transAxes, va='top', ha='left', fontsize=9,
        fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#eef2ff', edgecolor='steelblue', linewidth=1.2))

    ax_right.text(0.05, 0.95, _build_results_text(txt, results),
        transform=ax_right.transAxes, va='top', ha='left', fontsize=9,
        fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f0fff4', edgecolor='seagreen', linewidth=1.2))

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
    plt.savefig(output_dir / f"{case_id}_detalle_constructivo.pdf", format="pdf", bbox_inches="tight")
    # plt.show()