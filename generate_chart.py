#%%
# Script to generate Spain building renovation rate projection chart
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Historical data
historical_data = {
    'year': [2010, 2015, 2020, 2023],
    'renovation_rate': [0.2, 0.4, 0.6, 0.8],  # Percentage
    'energy_reduction': [5, 12, 18, 22],      # Percentage from 2005 baseline
    'investment_energy_efficiency': [500, 800, 1200, 1800]  # Million €/year
}

# Historical data
years = np.array(historical_data['year'])
rates = np.array(historical_data['renovation_rate'])

# Calculate BAU trajectory using linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(years, rates)

# Project future years
projection_years = np.arange(2010, 2031)
bau_trajectory = slope * projection_years + intercept

# EU Target (constant 3% line)
target_line = np.ones(len(projection_years)) * 3.0

# Calculate acceleration trajectory
# First part is historical (until 2023)
acceleration_trajectory = np.zeros(len(projection_years))
historical_idx = np.where(projection_years <= 2023)[0]
acceleration_trajectory[historical_idx] = [rates[list(years).index(y)] if y in years else np.nan for y in projection_years[historical_idx]]

# Second part is the required acceleration to meet target by 2030
current_rate = rates[-1]  # 0.8% in 2023
target_rate = 3.0  # 3% by 2030
years_to_target = 7  # 2023 to 2030
annual_increment = (target_rate - current_rate) / years_to_target

future_idx = np.where(projection_years > 2023)[0]
for i, year_idx in enumerate(future_idx):
    year = projection_years[year_idx]
    years_from_2023 = year - 2023
    acceleration_trajectory[year_idx] = current_rate + (annual_increment * years_from_2023)

# Create the plot
plt.figure(figsize=(12, 8))

# Plot the trajectories
plt.plot(projection_years, bau_trajectory, 'b-', linewidth=2, label='Business As Usual (BAU)')
plt.plot(projection_years, target_line, 'g-', linewidth=2, label='EU Target (3%)')
plt.plot(projection_years, acceleration_trajectory, 'r--', linewidth=3, label='Required Acceleration')

# Plot historical data points
plt.plot(years, rates, 'ko', markersize=8, label='Historical Data')

# Fill the gap area between BAU and required trajectory
plt.fill_between(projection_years[future_idx],
                 bau_trajectory[future_idx],
                 acceleration_trajectory[future_idx],
                 color='red', alpha=0.2, label='Implementation Gap')

# Annotations
plt.annotate(f"BAU by 2030: {bau_trajectory[-1]:.1f}%",
             xy=(2030, bau_trajectory[-1]),
             xytext=(2025, bau_trajectory[-1]-0.5),
             arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10)

plt.annotate(f"Gap: {target_line[-1] - bau_trajectory[-1]:.1f}%",
             xy=(2027, (target_line[-1] + bau_trajectory[-1])/2),
             xytext=(2020, (target_line[-1] + bau_trajectory[-1])/2),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10)

# Add details to the plot
plt.title('Spain Building Renovation Rate: Projections vs EU 2030 Target', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Renovation Rate (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(np.arange(2010, 2031, 2))
plt.yticks(np.arange(0, 4.1, 0.5))

# Add vertical line at current year
plt.axvline(x=2023, color='gray', linestyle='--')
plt.text(2023.2, 0.1, 'Current', rotation=90)

# Legend
plt.legend(loc='upper left', fontsize=10)

# Add explanatory text box
textstr = '\n'.join((
    'Key Insights:',
    f'• Current rate (2023): {rates[-1]:.1f}%',
    f'• BAU projection (2030): {bau_trajectory[-1]:.1f}%',
    f'• Required rate (2030): {target_line[-1]:.1f}%',
    f'• Annual acceleration needed: {annual_increment:.2f}% per year'
))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(2010.5, 2.5, textstr, fontsize=10, bbox=props)

plt.tight_layout()
# Save the figure to the images directory
plt.savefig('C:/dev/residential-energy-efficiency-stats/images/spain_renovation_rate_projections.png', dpi=300)
print("Chart saved to images/spain_renovation_rate_projections.png")
