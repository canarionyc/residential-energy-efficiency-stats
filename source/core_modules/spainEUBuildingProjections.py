# * ureg.pct* ureg.pct setup
import numpy as np
import matplotlib.pyplot as plt

# * ureg.pct* ureg.pct Conceptual projection framework
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from source.core_modules import ureg


class SpainEUBuildingProjections:
	def __init__(self):
		self.eu_targets = {
			'2030': {'renovation_rate': 3 * ureg.percent, 'energy_reduction': 55 * ureg.percent},
			'2050': {'carbon_neutral': True, 'renovation_rate': 100 * ureg.percent}
		}

		self.spain_baseline = {
			'current_renovation_rate': 0.8 * ureg.percent,  # 2023 data
			'epc_a_b_buildings': 12 * ureg.percent,  # High efficiency buildings
			'annual_new_construction': 1.2 * ureg.percent  # Of total stock
		}

	def calculate_trajectory(self):
		"""Calculate required acceleration to meet targets"""
		years_to_2030 = 7
		current_rate = self.spain_baseline['current_renovation_rate']
		target_rate = self.eu_targets['2030']['renovation_rate']

		# Linear acceleration needed
		annual_acceleration = (target_rate - current_rate) / years_to_2030
		return annual_acceleration

	def plot_trajectory_comparison(self, historical_data):
		"""
		Plot comparison of BAU baseline, target and acceleration trajectory

		Parameters:
		-----------
		historical_data : dict
			Dictionary containing historical renovation rate data with keys 'year' and 'renovation_rate'
		"""
		import numpy as np
		import matplotlib.pyplot as plt
		from scipy import stats

		# Convert historical data to arrays
		years = np.array(historical_data['year'])
		rates = np.array(historical_data['renovation_rate'])

		# Calculate BAU trajectory using linear regression
		slope, intercept, r_value, p_value, std_err = stats.linregress(years, rates)

		# Project future years
		projection_years = np.arange(min(years), 2031)
		bau_trajectory = slope * projection_years + intercept

		# EU Target (constant line at target value)
		target_line = np.ones(len(projection_years)) * (self.eu_targets['2030']['renovation_rate'].magnitude)

		# Calculate acceleration trajectory
		acceleration_trajectory = np.zeros(len(projection_years))
		current_year = max(years)
		current_rate = rates[-1]

		# Historical part
		historical_idx = np.where(projection_years <= current_year)[0]
		for i, idx in enumerate(historical_idx):
			year = projection_years[idx]
			if year in years:
				acceleration_trajectory[idx] = rates[list(years).index(year)]
			else:
				# Interpolate if needed
				acceleration_trajectory[idx] = np.nan

		# Future part - acceleration to meet target
		annual_acceleration = self.calculate_trajectory().magnitude
		future_idx = np.where(projection_years > current_year)[0]
		for i, idx in enumerate(future_idx):
			year = projection_years[idx]
			years_from_current = year - current_year
			acceleration_trajectory[idx] = current_rate + (annual_acceleration * years_from_current)

		# Create the plot
		plt.figure(figsize=(12, 8))

		# Plot the trajectories
		plt.plot(projection_years, bau_trajectory, 'b-', linewidth=2, label='Business As Usual (BAU)')
		plt.plot(projection_years, target_line, 'g-', linewidth=2, label=f'EU Target ({self.eu_targets["2030"]["renovation_rate"].magnitude}%)')
		plt.plot(projection_years, acceleration_trajectory, 'r--', linewidth=3, label='Required Acceleration')

		# Plot historical data points
		plt.plot(years, rates, 'ko', markersize=8, label='Historical Data')

		# Fill the gap area between BAU and required trajectory
		plt.fill_between(projection_years[future_idx],
					   bau_trajectory[future_idx],
					   acceleration_trajectory[future_idx],
					   color='red', alpha=0.2, label='Implementation Gap')

		# Add annotations
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
		plt.xticks(np.arange(min(projection_years), 2031, 2))
		plt.yticks(np.arange(0, 4.1, 0.5))

		# Add vertical line at current year
		plt.axvline(x=current_year, color='gray', linestyle='--')
		plt.text(current_year + 0.2, 0.1, 'Current', rotation=90)

		# Legend
		plt.legend(loc='upper left', fontsize=10)

		# Add explanatory text box
		textstr = '\n'.join((
			'Key Insights:',
			f'• Current rate ({current_year}): {rates[-1]:.1f}%',
			f'• BAU projection (2030): {bau_trajectory[-1]:.1f}%',
			f'• Required rate (2030): {target_line[-1]:.1f}%',
			f'• Annual acceleration needed: {annual_acceleration:.2f}% per year'
		))
		props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
		plt.text(min(projection_years) + 0.5, 2.5, textstr, fontsize=10, bbox=props)

		plt.tight_layout()
		return plt

if __name__ == "__main__":
	# Test the projection class
	sbp = SpainEUBuildingProjections()
	print(f"Annual acceleration needed: {sbp.calculate_trajectory()}")

	# Sample historical data for testing
	historical_data = {
		'year': [2010, 2015, 2020, 2023],
		'renovation_rate': [0.2, 0.4, 0.6, 0.8]  # Percentage
	}

	# Generate and show the plot
	plot = sbp.plot_trajectory_comparison(historical_data)
	# plot.savefig('spain_renovation_projections.png', dpi=300)
	# plot.show()
