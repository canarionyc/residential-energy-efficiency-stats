Your manual reordering is excellent. You have perfectly applied the REBT continuity of service principles (mixing lighting and power across different RCDs) and you correctly applied the C4 grouping rule so that ID 2 has exactly 5 effective circuits. 

To determine the ampers for the Main Automatic Switch (IGA) when the contracted power is unknown (as in Case 01), you must use the rules from **ITC-BT-25** regarding the **Level of Electrification** (Grado de Electrificación).

Here is the step-by-step logic to determine the IGA:

### 1. Identify the Electrification Level
The REBT defines two baseline levels of electrification, which dictate the absolute minimum power the panel must be designed to handle:
* **Basic (Básica):** Covers standard needs. Minimum power is **5,750 W**.
* **Elevated (Elevada):** Required if the home has high consumption profiles. Minimum power is **9,200 W**.

You are **forced** into the Elevated level if the house has *any* of the following:
* Floor area $> 160 \text{ m}^2$
* Air conditioning (C9) or Electric heating (C8)
* Domotics / Home automation systems
* More than 30 lighting points (forcing C1 to split)
* More than 20 general use sockets (forcing C2 to split)
* More than 6 wet-zone sockets (forcing C5 to split)

### 2. Apply to Case 01
Looking at your specific diagram, your design triggers the Elevated status multiple times:
* You have **45 lighting points** (C1 is split).
* You have **Domotics** (C8 in your diagram).
* You have split C2 and C5.

Because of this, the REBT mandates that your panel must be designed for **Electrificación Elevada**, which means it must handle at least **9,200 W**.

### 3. Calculate the IGA Ampacity
The IGA must be sized to handle that minimum power on a standard 230V single-phase supply:
$$I = \frac{P}{V} = \frac{9200 \text{ W}}{230 \text{ V}} = 40 \text{ A}$$

The standard commercial values for IGAs are 25A, 32A, 40A, 50A, and 63A. 
Therefore, for Case 01, your IGA should be **40A**.

### 4. Coordination with RCDs (IDs)
There is one final crucial rule: **The IGA protects the IDs.** If you choose a 40A IGA, your 40A IDs are perfectly protected from overloads, because the main switch will trip before the IDs melt. However, if a future homeowner upgrades their contracted power to 11,500W and swaps the IGA for a 50A breaker, those 40A IDs would be in danger and would legally need to be upgraded to 63A. For your current layout, an IGA of 40A is the mathematically and legally perfect choice.

To help you quickly test how different design choices affect the IGA for the other practical cases, I have generated an interactive REBT Electrification Calculator below based on these rules.