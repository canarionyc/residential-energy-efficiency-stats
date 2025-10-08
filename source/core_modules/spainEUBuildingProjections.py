#%% setup
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('C:/dev/residential-energy-efficiency-stats')
print(os.getcwd())
if not os.path.exists('figures'):
	os.makedirs('figures')

# %% Conceptual projection framework
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

	def plot_nextgenerationeu_impact(self, historical_data):
		"""
		Analyze and visualize the impact of NextGenerationEU funds on renovation trends,
		showing changepoint between 2016-2020 and 2021-2025 periods for both shallow
		and deep renovations.

		Parameters:
		-----------
		historical_data : dict
			Dictionary containing historical data with keys:
			- 'year': years from 2016-2025
			- 'shallow_renovation_rate': Percentage of shallow renovations by year
			- 'deep_renovation_rate': Percentage of deep renovations by year

		Returns:
		--------
		matplotlib.pyplot: Plot object
		"""
		# Set up figure
		plt.figure(figsize=(14, 10))

		# Extract data
		years = np.array(historical_data['year'])
		shallow_rates = np.array(historical_data['shallow_renovation_rate'])
		deep_rates = np.array(historical_data['deep_renovation_rate'])

		# Define periods
		pre_ngeu_mask = (years >= 2016) & (years <= 2020)
		post_ngeu_mask = (years >= 2021) & (years <= 2025)

		pre_ngeu_years = years[pre_ngeu_mask]
		post_ngeu_years = years[post_ngeu_mask]

		# Reshape arrays for sklearn
		X_pre = pre_ngeu_years.reshape(-1, 1)
		X_post = post_ngeu_years.reshape(-1, 1)

		# Create models for shallow renovations
		shallow_pre_ngeu = shallow_rates[pre_ngeu_mask]
		shallow_post_ngeu = shallow_rates[post_ngeu_mask]

		shallow_model_pre = LinearRegression()
		shallow_model_pre.fit(X_pre, shallow_pre_ngeu)
		shallow_r2_pre = r2_score(shallow_pre_ngeu, shallow_model_pre.predict(X_pre))

		shallow_model_post = LinearRegression()
		shallow_model_post.fit(X_post, shallow_post_ngeu)
		shallow_r2_post = r2_score(shallow_post_ngeu, shallow_model_post.predict(X_post))

		# Create models for deep renovations
		deep_pre_ngeu = deep_rates[pre_ngeu_mask]
		deep_post_ngeu = deep_rates[post_ngeu_mask]

		deep_model_pre = LinearRegression()
		deep_model_pre.fit(X_pre, deep_pre_ngeu)
		deep_r2_pre = r2_score(deep_pre_ngeu, deep_model_pre.predict(X_pre))

		deep_model_post = LinearRegression()
		deep_model_post.fit(X_post, deep_post_ngeu)
		deep_r2_post = r2_score(deep_post_ngeu, deep_model_post.predict(X_post))

		# Calculate slopes (annual percentage point change)
		shallow_slope_pre = shallow_model_pre.coef_[0]
		shallow_slope_post = shallow_model_post.coef_[0]
		deep_slope_pre = deep_model_pre.coef_[0]
		deep_slope_post = deep_model_post.coef_[0]

		# Calculate percentage increase in slopes
		shallow_slope_increase = ((shallow_slope_post - shallow_slope_pre) / abs(shallow_slope_pre)) * 100
		deep_slope_increase = ((deep_slope_post - deep_slope_pre) / abs(deep_slope_pre)) * 100

		# Create continuous prediction lines for visualization
		X_pre_cont = np.linspace(2016, 2020, 100).reshape(-1, 1)
		X_post_cont = np.linspace(2021, 2025, 100).reshape(-1, 1)

		shallow_pred_pre = shallow_model_pre.predict(X_pre_cont)
		shallow_pred_post = shallow_model_post.predict(X_post_cont)
		deep_pred_pre = deep_model_pre.predict(X_pre_cont)
		deep_pred_post = deep_model_post.predict(X_post_cont)

		# Plotting
		plt.subplot(2, 1, 1)
		# Plot data points
		plt.scatter(years[pre_ngeu_mask], shallow_rates[pre_ngeu_mask], color='blue', s=60, alpha=0.7,
				   label='Shallow Renovations (Pre-NextGenEU)')
		plt.scatter(years[post_ngeu_mask], shallow_rates[post_ngeu_mask], color='blue', s=80, marker='D', alpha=0.9,
				   label='Shallow Renovations (Post-NextGenEU)')

		# Plot regression lines
		plt.plot(X_pre_cont, shallow_pred_pre, 'b--', linewidth=2,
				label=f'Pre-NextGenEU Trend (R²={shallow_r2_pre:.2f}, Slope={shallow_slope_pre:.2f}%/yr)')
		plt.plot(X_post_cont, shallow_pred_post, 'b-', linewidth=3,
				label=f'Post-NextGenEU Trend (R²={shallow_r2_post:.2f}, Slope={shallow_slope_post:.2f}%/yr)')

		# Add vertical line for NextGenEU start
		plt.axvline(x=2020.5, color='green', linestyle='-', linewidth=2, alpha=0.7)
		plt.text(2020.6, max(shallow_rates)*0.8, 'NextGenerationEU\nImplementation',
				fontsize=10, color='green', fontweight='bold')

		plt.title('Impact of NextGenerationEU on Shallow Renovation Rates in Spain', fontsize=14)
		plt.xlabel('Year', fontsize=12)
		plt.ylabel('Shallow Renovation Rate (%)', fontsize=12)
		plt.grid(True, linestyle='--', alpha=0.6)
		plt.legend(loc='upper left', fontsize=10)

		# Add annotation about slope change
		plt.annotate(f"Slope increased by {shallow_slope_increase:.1f}%",
				   xy=(2023, shallow_pred_post[-1]),
				   xytext=(2022, shallow_pred_post[-1] - 0.5),
				   arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
				   fontsize=10)

		# Second subplot for deep renovations
		plt.subplot(2, 1, 2)
		# Plot data points
		plt.scatter(years[pre_ngeu_mask], deep_rates[pre_ngeu_mask], color='red', s=60, alpha=0.7,
				   label='Deep Renovations (Pre-NextGenEU)')
		plt.scatter(years[post_ngeu_mask], deep_rates[post_ngeu_mask], color='red', s=80, marker='D', alpha=0.9,
				   label='Deep Renovations (Post-NextGenEU)')

		# Plot regression lines
		plt.plot(X_pre_cont, deep_pred_pre, 'r--', linewidth=2,
				label=f'Pre-NextGenEU Trend (R²={deep_r2_pre:.2f}, Slope={deep_slope_pre:.2f}%/yr)')
		plt.plot(X_post_cont, deep_pred_post, 'r-', linewidth=3,
				label=f'Post-NextGenEU Trend (R²={deep_r2_post:.2f}, Slope={deep_slope_post:.2f}%/yr)')

		# Add vertical line for NextGenEU start
		plt.axvline(x=2020.5, color='green', linestyle='-', linewidth=2, alpha=0.7)
		plt.text(2020.6, max(deep_rates)*0.8, 'NextGenerationEU\nImplementation',
				fontsize=10, color='green', fontweight='bold')

		plt.title('Impact of NextGenerationEU on Deep Renovation Rates in Spain', fontsize=14)
		plt.xlabel('Year', fontsize=12)
		plt.ylabel('Deep Renovation Rate (%)', fontsize=12)
		plt.grid(True, linestyle='--', alpha=0.6)
		plt.legend(loc='upper left', fontsize=10)

		# Add annotation about slope change
		plt.annotate(f"Slope increased by {deep_slope_increase:.1f}%",
				   xy=(2023, deep_pred_post[-1]),
				   xytext=(2022, deep_pred_post[-1] - 0.3),
				   arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
				   fontsize=10)

		# Add explanatory text box
		textstr = '\n'.join((
			'NextGenerationEU Impact:',
			f'• Shallow renovations: {shallow_slope_increase:.1f}% slope increase',
			f'• Deep renovations: {deep_slope_increase:.1f}% slope increase',
			f'• Deep/Shallow ratio before: {deep_pre_ngeu.mean()/shallow_pre_ngeu.mean():.2f}',
			f'• Deep/Shallow ratio after: {deep_post_ngeu.mean()/shallow_post_ngeu.mean():.2f}'
		))
		props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
		plt.text(2016.2, max(deep_rates)*0.5, textstr, fontsize=10, bbox=props)

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
	plot.savefig('figures/spain_renovation_projections.png', dpi=300)
	plot.show()

	# Sample data for NextGenerationEU impact analysis
	ngeu_impact_data = {
		'year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
		'shallow_renovation_rate': [0.6, 0.65, 0.7, 0.72, 0.75, 0.85, 1.0, 1.2, 1.35, 1.5],  # Percentage
		'deep_renovation_rate': [0.1, 0.12, 0.15, 0.17, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95]     # Percentage
	}

	# Generate and show the NextGenerationEU impact analysis
	ngeu_plot = sbp.plot_nextgenerationeu_impact(ngeu_impact_data)
	ngeu_plot.savefig('figures/spain_nextgeneu_impact.png', dpi=300)
	ngeu_plot.show()
