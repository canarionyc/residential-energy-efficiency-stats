# %% setup
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('C:/dev/residential-energy-efficiency-stats')
print(os.getcwd())
#%%
# Spain's energy mix data 2023
energy_sources = ['Oil/Petroleum', 'Gas', 'Nuclear', 'Renewables']
percentages = [42.3, 19.8, 9.6, 25.7]
colors = ['#ff9e00', '#3498db', '#9b59b6', '#2ecc71']

# Buildings energy consumption data
buildings_spain = 31.2
buildings_eu = 39.5

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('Spain Energy Statistics 2023', fontsize=16)

# Plot 1: Energy mix pie chart
ax1.pie(percentages, labels=energy_sources, autopct='%1.1f%%',
        startangle=90, colors=colors, shadow=False)
ax1.set_title('Energy Mix Distribution')

# Plot 2: Buildings energy consumption comparison
x = ['Spain', 'EU Average']
y = [buildings_spain, buildings_eu]
bars = ax2.bar(x, y, color=['#e74c3c', '#3498db'])
ax2.bar_label(bars, fmt='%.1f%%')
ax2.set_ylim(0, 50)
ax2.set_title('Energy Consumption in Buildings')
ax2.set_ylabel('Percentage of Total Energy Consumption')

plt.tight_layout()
plt.savefig('images/spain_energy_mix_2023.png', dpi=300, bbox_inches='tight')
plt.show()
