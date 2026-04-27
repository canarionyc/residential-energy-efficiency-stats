#%% BILINGUAL CONFIGURATION
import json

LANG = "ES"  # Toggle to "ES" for Spanish labels

# Emulating the requested plot JSON structure for terminal output formatting
output_config = {
    "EN": {
        "title": "REBT RCD CIRCUIT COUNTER",
        "rcd_label": "RCD",
        "effective_count": "Effective RCD Count",
        "physical_count": "Physical PIAs",
        "status_ok": "OK (<= 5)",
        "status_fail": "FAIL (> 5)",
        "c4_grouping": "C4 split detected: counting as 1."
    }
}

if LANG == "ES":
    output_config["ES"] = {
        "title": "CONTADOR DE CIRCUITOS ID REBT",
        "rcd_label": "Diferencial (ID)",
        "effective_count": "Conteo Efectivo ID",
        "physical_count": "PIAs Físicos",
        "status_ok": "CORRECTO (<= 5)",
        "status_fail": "ERROR (> 5)",
        "c4_grouping": "Desdoblamiento C4 detectado: se contabiliza como 1."
    }
    labels = output_config["ES"]
else:
    labels = output_config["EN"]


#%% REBT SMART RCD GROUP
# class Circuit:
#     def __init__(self, c_type, description):
#         self.c_type = c_type
#         self.description = description

class SmartRCDGroup:
    def __init__(self, rcd_id):
        self.rcd_id = rcd_id
        self.circuits = []

    def add(self, circuit):
        self.circuits.append(circuit)

    def get_effective_count(self):
        """
        Calculates the number of circuits according to REBT ITC-BT-25.
        Multiple C4 circuits (Lavadora, Lavavajillas, Termo) count as 1.
        """
        types_present = [c.c_type for c in self.circuits]

        # Count non-C4 circuits normally
        effective_count = len([t for t in types_present if t != "C4"])

        # If any C4 circuits exist, they collectively add exactly 1 to the count
        if "C4" in types_present:
            effective_count += 1

        return effective_count

    def validate(self):
        eff_count = self.get_effective_count()
        phys_count = len(self.circuits)
        status = labels["status_ok"] if eff_count <= 5 else labels["status_fail"]

        print(f"[{labels['rcd_label']} {self.rcd_id}]")
        print(f" - {labels['physical_count']}: {phys_count}")
        print(f" - {labels['effective_count']}: {eff_count} -> {status}")

        if "C4" in [c.c_type for c in self.circuits] and phys_count > eff_count:
            print(f"   * {labels['c4_grouping']}")
        print("-" * 30)


#%% EXECUTION DEMONSTRATION
if __name__ == "__main__":
    print(f"=== {labels['title']} ===\n")

    # Re-evaluating the RCD 2 from Case 1
    rcd_2 = SmartRCDGroup("2 (Caso 1)")
    rcd_2.add(Circuit("C3", "Cocina/Horno"))
    rcd_2.add(Circuit("C4", "Lavadora"))
    rcd_2.add(Circuit("C4", "Lavavajillas"))
    rcd_2.add(Circuit("C4", "Termo"))
    rcd_2.add(Circuit("C5", "Baño tomas"))
    rcd_2.add(Circuit("C5", "Cocina tomas"))

    rcd_2.validate()