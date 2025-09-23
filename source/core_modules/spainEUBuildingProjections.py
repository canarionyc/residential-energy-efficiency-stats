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

if __name__ == "__main__":
	sbp = SpainEUBuildingProjections()
	print(sbp.calculate_trajectory())