"""
pyCTE - Python implementation of Codigo Tecnico de la Edificacion (CTE)
for Building Energy Efficiency.
"""

__version__ = '0.1.0'

import pint

# Create a single unit registry for the entire package
ureg = pint.UnitRegistry()

# Define Quantity as a shorthand for creating quantities
Quantity = ureg.Quantity

# Import commonly used functions for easier access
# from .core_modules.module1 import function1, function2
# from .core_modules.module2 import ClassA, ClassB

# Export the registry and Quantity for use in other modules
__all__ = ['ureg', 'Quantity']