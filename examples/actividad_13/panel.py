# %% ADVANCED PANEL CLASS WITH AUDIT CAPABILITIES

from rcd_group import RCDGroup
from circuit import Circuit
from constants import LANG, labels

# Assuming LANG is imported or defined globally
PANEL_LABELS = {
    "EN": {
        "main_panel": "MAIN DISTRIBUTION PANEL (CDMP)",
        "sub_panel": "SUB-PANEL",
        "stats_title": "CIRCUIT TYPE BREAKDOWN & AUDIT",
        "feeder": "Feeder Line",
        "phys_pias": "Total Physical PIAs",
        "max_rcd": "Max RCD Load (Effective)",
        "design_pwr": "Design Power",
        "summary": "BUILDING SUMMARY REPORT",
        "local": "Local Stats for"
    },
    "ES": {
        "main_panel": "CUADRO GENERAL (CDMP)",
        "sub_panel": "SUBCUADRO",
        "stats_title": "DESGLOSE POR TIPO Y AUDITORÍA",
        "feeder": "Línea Repartidora",
        "phys_pias": "Total PIAs Físicos",
        "max_rcd": "Carga Máx. en un ID (Efectivos)",
        "design_pwr": "Potencia de Diseño",
        "summary": "RESUMEN GENERAL DE LA EDIFICACIÓN",
        "local": "Estadísticas Locales de"
    }
}
p_labels = PANEL_LABELS[LANG]


class Panel:
    def __init__(self, name, power_w: float=None):
        self.name = name
        self.power_w = power_w
        self.iga_amps = self._estimate_iga()
        self.rcd_groups = []

    def _estimate_iga(self):
        if not self.power_w: return "A Determinar"
        current = self.power_w / 230
        for std_iga in [25, 32, 40, 50, 63]:
            if std_iga >= current: return std_iga
        return 63

    def add_rcd(self, rcd_group : RCDGroup):
        self.rcd_groups.append(rcd_group)

    def generate_audit_report(self):
        # 1. Aggregation Dictionary: { "C1": {"points": 0, "count": 0}, ... }
        stats = {}
        total_physical_pias = 0
        effective_rcd_counts = []  # List of effective counts per RCD

        for rcd in self.rcd_groups:
            # We use the smart counting logic for RCD compliance
            types_in_rcd = [c.c_type for c in rcd.circuits]
            eff_count = len([t for t in types_in_rcd if t != "C4"])
            if "C4" in types_in_rcd: eff_count += 1
            effective_rcd_counts.append(eff_count)

            for circ in rcd.circuits:
                total_physical_pias += 1
                if circ.c_type not in stats:
                    stats[circ.c_type] = {"points": 0, "count": 0, "desc": circ.desc}
                stats[circ.c_type]["points"] += circ.points
                stats[circ.c_type]["count"] += 1

        # 2. Rendering the Breakdown Table
        headers = {
            "EN": ["Type", "Total Pts", "PIA Count", "Typical Use"],
            "ES": ["Tipo", "Puntos Tot", "Num. PIAs", "Uso Típico"]
        }[LANG]

        print(f"\n{'=' * 70}")
        print(f" {self.name} - {labels['stats_title']} ")
        print(f"{'=' * 70}")
        print(f"{headers[0]:<6} | {headers[1]:<10} | {headers[2]:<10} | {headers[3]}")
        print("-" * 70)

        # Sort by circuit number (C1, C2, C3...)
        for c_type in sorted(stats.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)):
            data = stats[c_type]
            print(f"{c_type:<6} | {data['points']:<10} | {data['count']:<10} | {data['desc']}")

        # 3. Final Compliance Summary
        print("-" * 70)
        summary_labels = {
            "EN": [
                f"Total Physical PIAs:  {total_physical_pias}",
                f"Max RCD Load:         {max(effective_rcd_counts) if effective_rcd_counts else 0} / 5",
                f"Design Power:         {self.power_w} W"
            ],
            "ES": [
                f"Total PIAs Físicos:   {total_physical_pias}",
                f"Carga Máx. en un ID:  {max(effective_rcd_counts) if effective_rcd_counts else 0} / 5",
                f"Potencia de Diseño:   {self.power_w} W"
            ]
        }[LANG]

        for line in summary_labels:
            print(line)
        print(f"{'=' * 70}\n")

    def render(self):

        print(f"\n{'='*60}\n[{labels['panel']}] {self.name}")
        print(f"  |-- [{labels['iga']}] {self.iga_amps}A")

        for rcd in self.rcd_groups:
            print("       |")
            print(f"       +-- [{labels['rcd']} {rcd.rcd_id}] 40A/30mA")
            for j, circ in enumerate(rcd.circuits):
                branch = "    +--" if j == len(rcd.circuits)-1 else "    |--"
                print(f"            {branch} {circ}")
        print("="*60)


# %% EXECUTION EXAMPLE (Using Case 4 Data)
if __name__ == "__main__":
    LANG="ES"
    # We reuse the logic from the previous driver to populate a test panel
    test_panel = Panel("AUDIT TEST CASE 04", 5750)

    # Simulating a split that might fail or pass
    r1 = RCDGroup("1")
    r1.add(Circuit("C1", "Alumbrado Salón", points=33))  # This should trigger "FAIL"
    r1.add(Circuit("C2", "Enchufes Cocina", points=16))

    test_panel.add_rcd(r1)

    # Generate the statistics table
    test_panel.generate_audit_report()