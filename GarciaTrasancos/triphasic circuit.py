#%% Initialization and Configuration
import numpy as np
import matplotlib.pyplot as plt
import json

# Toggle switch for bilingual plot output
LANG = 'ES' # Change to 'EN' for English

# Dictionary for bilingual plot text
plot_text_dict = {
    'EN': {
        'title': 'Phasor Diagram: Balanced Three-Phase Star Connection',
        'xlabel': 'Real Axis',
        'ylabel': 'Imaginary Axis',
        'legend_V': 'Phase Voltages (V)',
        'legend_I': 'Line Currents (A x10 for visibility)',
        'annotation_V1': 'V1 (R)',
        'annotation_V2': 'V2 (S)',
        'annotation_V3': 'V3 (T)',
        'annotation_I1': 'I1',
        'annotation_I2': 'I2',
        'annotation_I3': 'I3'
    },
    'ES': {
        'title': 'Diagrama Fasorial: Carga Trifásica Equilibrada en Estrella',
        'xlabel': 'Eje Real',
        'ylabel': 'Eje Imaginario',
        'legend_V': 'Tensiones de Fase (V)',
        'legend_I': 'Corrientes de Línea (A x10 para visibilidad)',
        'annotation_V1': 'V1 (R)',
        'annotation_V2': 'V2 (S)',
        'annotation_V3': 'V3 (T)',
        'annotation_I1': 'I1',
        'annotation_I2': 'I2',
        'annotation_I3': 'I3'
    }
}

labels = plot_text_dict.get(LANG, plot_text_dict['EN'])

# %% System Definition and Calculations
# 1. Define standard grid parameters (European / Spanish REBT standard)
V_line_rms = 400.0  # Line-to-line voltage (V_L)
f = 50.0            # Frequency in Hz

# Phase voltage in a star connection is V_L / sqrt(3)
V_phase_rms = V_line_rms / np.sqrt(3)

# 2. Define the load per phase (Impedance Z = R + jX)
# For this baseline, we use an inductive load (e.g., an AC motor)
R = 8.0  # Resistance in Ohms
X = 6.0  # Reactance in Ohms
Z = complex(R, X)

print(f"Phase Voltage (Magnitude): {V_phase_rms:.2f} V")
print(f"Impedance per phase: {np.abs(Z):.2f} Ohms, Angle: {np.degrees(np.angle(Z)):.2f} degrees")

# 3. Calculate Voltage Phasors (120 degrees apart)
# R, S, T phases are mathematically represented as complex exponentials
V1 = V_phase_rms * np.exp(1j * np.deg2rad(0))
V2 = V_phase_rms * np.exp(1j * np.deg2rad(-120))
V3 = V_phase_rms * np.exp(1j * np.deg2rad(120))

# 4. Calculate Current Phasors (Ohm's law for AC: I = V / Z)
I1 = V1 / Z
I2 = V2 / Z
I3 = V3 / Z

print(f"Line Current (Magnitude): {np.abs(I1):.2f} A")
print(f"Power Factor (cos phi): {np.cos(np.angle(Z)):.2f}")

#%% Phasor Diagram Plotting
fig, ax = plt.subplots(figsize=(8, 8))

# Helper function to plot phasors
def plot_phasor(ax, complex_val, color, label_text, scale=1.0):
    x = complex_val.real * scale
    y = complex_val.imag * scale
    ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color, width=0.005)
    ax.text(x * 1.1, y * 1.1, label_text, color=color, fontsize=12, fontweight='bold')

# Plot Voltages
plot_phasor(ax, V1, 'red', labels['annotation_V1'])
plot_phasor(ax, V2, 'black', labels['annotation_V2'])
plot_phasor(ax, V3, 'blue', labels['annotation_V3'])

# Plot Currents (Scaled by 10 so they are visible alongside the 230V vectors)
scale_I = 10
plot_phasor(ax, I1, 'lightcoral', labels['annotation_I1'], scale_I)
plot_phasor(ax, I2, 'gray', labels['annotation_I2'], scale_I)
plot_phasor(ax, I3, 'cornflowerblue', labels['annotation_I3'], scale_I)

# Formatting the plot
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)

# Calculate limits for aesthetic plotting
limit = max(np.abs(V1), np.abs(I1)*scale_I) * 1.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')

# Add labels and grid
ax.set_title(labels['title'], fontsize=14, pad=20)
ax.set_xlabel(labels['xlabel'])
ax.set_ylabel(labels['ylabel'])
ax.grid(True, alpha=0.3)

# Custom legend
ax.plot([], [], color='red', label=labels['legend_V'])
ax.plot([], [], color='lightcoral', label=labels['legend_I'])
ax.legend(loc='lower right')

plt.show()