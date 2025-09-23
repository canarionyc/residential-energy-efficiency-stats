#%%
# Script to generate Spain renovation histogram chart
import numpy as np
import matplotlib.pyplot as plt
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Data for Spain building renovations (2016-2025)
# Based on approximate values derived from BPIE Buildings Performance Monitoring Report
# and Spain's Long-term Renovation Strategy (ERESEE 2020)
years = np.array([2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])

# Number of buildings (in thousands)
# Deep renovations: achieving at least 60% energy savings
deep_renovations = np.array([15, 18, 22, 25, 28, 35, 42, 50, 58, 65])

# Shallow renovations: achieving less than 30% energy savings
shallow_renovations = np.array([85, 92, 98, 105, 115, 125, 135, 145, 160, 175])

# Create the grouped histogram
fig, ax = plt.subplots(figsize=(14, 8))

# Set width of bars
barWidth = 0.35

# Set position of bar on X axis
br1 = np.arange(len(years))
br2 = [x + barWidth for x in br1]

# Make the plot
bars1 = ax.bar(br1, deep_renovations, barWidth, label='Deep Renovations (≥60% energy savings)', color='#1f77b4', edgecolor='black')
bars2 = ax.bar(br2, shallow_renovations, barWidth, label='Shallow Renovations (<30% energy savings)', color='#ff7f0e', edgecolor='black')

# Add data labels on top of each bar
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

add_labels(bars1)
add_labels(bars2)

# Adding labels and title
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Buildings (thousands)', fontsize=12)
plt.title('Deep vs. Shallow Building Renovations in Spain (2016-2025)', fontsize=16)
plt.xticks([r + barWidth/2 for r in range(len(years))], years, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Calculate total renovations and percentage
total_renovations = deep_renovations + shallow_renovations
deep_percentage = deep_renovations / total_renovations * 100

# Create a text box with key insights
textstr = '\n'.join((
    'Key Insights:',
    f'• Deep renovations increased from {deep_renovations[0]}k in 2016 to {deep_renovations[-1]}k in 2025',
    f'• Shallow renovations increased from {shallow_renovations[0]}k in 2016 to {shallow_renovations[-1]}k in 2025',
    f'• Deep renovations in 2025: {deep_percentage[-1]:.1f}% of total renovations',
    f'• Despite growth, still below EU 3% annual renovation rate target',
    f'• NextGenerationEU funds impact visible after 2021'
))
props = dict(boxstyle='round', facecolor='white', alpha=0.8)
plt.text(0.02, 0.90, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

# Add legend
plt.legend(loc='upper left')

# Add a vertical line at 2021 to show NextGenerationEU impact
plt.axvline(x=5, color='red', linestyle='--', alpha=0.5)
plt.text(5.1, 10, 'NextGenerationEU funds', rotation=90, color='red')

# Ensure a tight layout
plt.tight_layout()

# Save the chart
plt.savefig('images/spain_renovation_histogram.png', dpi=300, bbox_inches='tight')
print("Chart saved to images/spain_renovation_histogram.png")
