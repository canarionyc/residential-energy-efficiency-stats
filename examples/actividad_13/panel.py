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
    def __init__(self, name, power_w=None, is_main=True, feeder_len=0):
        self.name = name
        self.power_w = power_w
        self.is_main = is_main
        self.feeder_len = feeder_len
        self.rcd_groups = []
        self.sub_panels = []
        self.iga_amps = self._estimate_iga()


    def _estimate_iga(self):
        if not self.power_w: return "A Determinar"
        current = self.power_w / 230
        for std_iga in [25, 32, 40, 50, 63]:
            if std_iga >= current: return std_iga
        return 63

    def add_sub_panel(self, sub):
        self.sub_panels.append(sub)

    def add_rcd(self, rcd_group : RCDGroup):
        self.rcd_groups.append(rcd_group)

    def get_aggregated_stats(self):
        """Recursively collects stats from this panel and all sub-panels."""
        # Initial local stats
        aggregate = {}
        total_phys = 0

        # 1. Process local circuits
        for rcd in self.rcd_groups:
            for circ in rcd.circuits:
                total_phys += 1
                if circ.c_type not in aggregate:
                    aggregate[circ.c_type] = {"points": 0, "count": 0, "desc": circ.desc}
                aggregate[circ.c_type]["points"] += circ.points
                aggregate[circ.c_type]["count"] += 1

        # 2. Recurse into sub-panels
        for sub in self.sub_panels:
            sub_stats, sub_phys = sub.get_aggregated_stats()
            total_phys += sub_phys
            for c_type, data in sub_stats.items():
                if c_type not in aggregate:
                    aggregate[c_type] = data
                else:
                    aggregate[c_type]["points"] += data["points"]
                    aggregate[c_type]["count"] += data["count"]

        return aggregate, total_phys

    def generate_audit_report(self):
        agg_stats, total_phys = self.get_aggregated_stats()

        print(f"\n{'=' * 75}")
        print(f" {p_labels['summary'] if self.is_main else p_labels['local']} {self.name} ")
        print(f"{'=' * 75}")

        # Header for the breakdown
        # [Using your logic for headers...]
        print(f"{'Tipo':<6} | {'Puntos':<10} | {'PIAs':<6} | {'Uso Típico'}")
        print("-" * 75)

        for c_type in sorted(agg_stats.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)):
            d = agg_stats[c_type]
            print(f"{c_type:<6} | {d['points']:<10} | {d['count']:<6} | {d['desc']}")

        print("-" * 75)
        print(f"{p_labels['phys_pias']}: {total_phys}")
        if self.power_w:
            print(f"{p_labels['design_pwr']}: {self.power_w} W")
        print(f"{'=' * 75}\n")

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