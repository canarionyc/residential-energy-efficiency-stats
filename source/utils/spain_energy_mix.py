# %% setup
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('C:/dev/residential-energy-efficiency-stats')
print(os.getcwd())
if not os.path.exists('images'):
	os.makedirs('images')
#%% ENERGY CONSUMPTION (2023): 31.2% of all primary energy consumed in Spain is in buildings (compared to EU average of
#%% 39.5%). The distribution in share of gross energy available in Spain was 42.3% oil/petroleum, 19.8% gas, 9.6% nuclear,
#%% and 25.7% renewables in 2023. A record high share for renewables, contributing to Spain's progress toward EU efficiency
#%% targets. ([Eurostat, 2024](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Energy_statistics_-_an_overview#Primary_energy_production)


# %% figures
# Ensure figures directory exists


# %% Energy statistics data by source
# Spain's energy mix data 2023
energy_sources = ['Oil/Petroleum', 'Gas', 'Nuclear', 'Renewables']
percentages = [42.3, 19.8, 9.6, 25.7]
colors_energy = ['#ff9e00', '#3498db', '#9b59b6', '#2ecc71']

# %% Approximate Distribution of Gross Available Energy in Spain (by sector)
# Transport: ~40%
#
# This is the largest consuming sector in Spain. It includes road transport (cars, trucks), aviation, maritime transport, and rail. The high share is influenced by Spain's significant tourism industry (requiring air and road transport) and its role as a logistics hub for Europe.
#
# Industry: ~25%
#
# This includes energy consumed by manufacturing, construction, and mining. Compared to the EU average, Spain's industrial share is slightly lower, reflecting a economic structure more focused on services and tourism.
#
# Households (Residential): ~17%
#
# This covers energy used in homes for heating, cooling, hot water, cooking, and appliances.
#
# Services (Commercial & Public Services): ~15%
#
# This sector includes energy used in offices, retail stores, hotels, restaurants, hospitals, and educational institutions. Spain's strong service and tourism economy contributes significantly to this share.
#
# Other (including Agriculture & Fishing): ~3%
#
# This is a smaller but still important sector, covering energy use in agriculture and fishing.

#%% Buildings energy consumption data by sector
buildings_labels = ['Transport', 'Industry','Households (Residential)','Services (Commercial & Public Services)',' Other (including Agriculture & Fishing)']
buildings_spain = [40, 25, 17, 15, 3]  # Buildings vs other sectors

#  For comparison, the EU-27 average distribution is roughly:
#
# Transport: ~30-32%
#
# Industry: ~26-28%
#
# Households: ~26%
#
# Services: ~14-15%
buildings_eu = [31,27,26,14.5,2.5]  # Buildings vs other sectors
colors_buildings = ['#e74c3c', '#7f8c8d', '#3498db', '#9b59b6', '#2ecc71']

# %% Create visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('Energy Consumption by Sector 2023', fontsize=16)

# Plot 1: Energy consumption by sector in Spain (left)
ax1.pie(buildings_spain, labels=buildings_labels, autopct='%1.1f%%',
	startangle=90, colors=colors_buildings, shadow=False)
ax1.set_title('Spain')

# Plot 2: Energy consumption by sector in EU27 (left)
ax2.pie(buildings_eu, labels=buildings_labels, autopct='%1.1f%%',
	startangle=90, colors=colors_buildings, shadow=False)
ax2.set_title('EU27')

#
# # Plot 2: Energy mix pie chart (right)
# ax2.pie(percentages, labels=energy_sources, autopct='%1.1f%%',
# 	startangle=90, colors=colors_energy, shadow=False)
# ax2.set_title('Energy Mix Distribution')

# Add a note about EU average
# fig.text(0.01, 0.01, f'Note: EU average for building energy consumption is {buildings_eu[0]}%',
# 	fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('figures/spain_energy_mix_2023.png', dpi=300, bbox_inches='tight')
plt.show()
