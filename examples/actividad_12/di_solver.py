# %% [markdown]
# # DI Solver Module
# Calculates Individual Derivation cross-sections according to REBT.

# %%
import math


class DISolver:
    """
    Engine to calculate the required cable cross-section for an Individual Derivation (DI).
    """

    def __init__(self, case_data):
        self.case_id = case_data.get("id", "Unknown")
        self.power = case_data["power_w"]
        self.length = case_data["length_m"]
        self.system = case_data["system"]
        self.temp = case_data["temp_c"]
        self.num_di = case_data["num_di"]

        # Standard constants for residential (Single-phase 230V)
        self.voltage = 230
        self.conductivity_cu = 56  # m/(Ohm*mm^2) for Copper
        self.max_vd_percent = 0.015  # 1.5% max voltage drop per ITC-BT-15

    def get_thermal_limit(self):
        """
        Calculates the theoretical minimum section based on current carrying capacity.
        Note: In a full engine, this would interpolate standard tables (ITC-BT-19)
        using self.system (B1/A1), self.temp, and self.num_di grouping factors.
        """
        # 1. Calculate design current (Ib)
        current = self.power / self.voltage

        # Placeholder for the actual REBT Table interpolation logic
        # For demonstration, assuming a rough approximation of 5A per mm^2
        theoretical_section = current / 5.0

        return theoretical_section

    def get_voltage_drop(self):
        """
        Calculates the required section S to keep voltage drop <= 1.5%.
        """
        # Maximum allowed voltage drop in Volts
        max_vd_volts = self.voltage * self.max_vd_percent

        # Single-phase voltage drop formula: S = (2 * L * P) / (C * e * V)
        section = (2 * self.length * self.power) / (self.conductivity_cu * max_vd_volts * self.voltage)

        return section

    def get_minimum_regulatory_section(self):
        """
        Returns the hardcoded minimums according to ITC-BT-15.
        """
        return 6.0  # 6 mm^2 is the absolute minimum for Phase/Neutral

    def solve(self):
        """
        Executes the three criteria and returns the limiting (maximum) cross-section.
        Rounds up to the nearest standard commercial cable size.
        """
        s_thermal = self.get_thermal_limit()
        s_voltage = self.get_voltage_drop()
        s_regulatory = self.get_minimum_regulatory_section()

        # The physical requirement is the strictest (maximum) of the three
        required_section = max(s_thermal, s_voltage, s_regulatory)

        # Standard commercial sections (mm^2)
        standard_sections = [6, 10, 16, 25, 35, 50, 70]

        final_section = next(s for s in standard_sections if s >= required_section)

        return {
            "case_id": self.case_id,
            "s_thermal": round(s_thermal, 2),
            "s_voltage": round(s_voltage, 2),
            "s_regulatory": round(s_regulatory, 2),
            "final_commercial_section": final_section
        }


#%% print results
def print_results(results):
    print(f"Results for {results['case_id']}:")
    print(f" - Section by Thermal Limit: {results['s_thermal']} mm^2")
    print(f" - Section by Voltage Drop:  {results['s_voltage']} mm^2")
    print(f" - Minimum Regulatory:       {results['s_regulatory']} mm^2")
    print(f" -> FINAL CABLE SECTION:     {results['final_commercial_section']} mm^2")

#%% print results ES
def print_results_ES(results):
    print(f"Results for {results['case_id']}:")
    print(f" - Section by Thermal Limit: {results['s_thermal']} mm^2")
    print(f" - Section by Voltage Drop:  {results['s_voltage']} mm^2")
    print(f" - Minimum Regulatory:       {results['s_regulatory']} mm^2")
    print(f" -> FINAL CABLE SECTION:     {results['final_commercial_section']} mm^2")

# %%  Caso 1
case_01_data = {
    "id": "CASE_01",
    "electrification": "Elevado",
    "system": "B1",
    "length_m": 12,
    "power_w": 5750,
    "temp_c": 30,
    "num_di": 9
}

solver = DISolver(case_01_data)
results = solver.solve()
print_results(results)

case_results={**case_01_data,**results }
print_results(case_results)

# Generate the plot for Case 01 (9 DIs, assuming 32mm tubes for example)
plot_conduit_detail(cases["CASE_01"]["num_di"], 32, "CASE_01")

#%% caso 2
case_data = cases['CASE_02']
print(f"Case 2: {case_data}")
solver = DISolver(case_data)
print_results(solver.solve())

#%% caso 3
case_data = cases['CASE_03']
print(f"Case 3: {case_data}")
solver = DISolver(case_data)
print_results(solver.solve())