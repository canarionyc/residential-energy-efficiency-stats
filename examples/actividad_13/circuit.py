from constants import REBT_CATALOG, STANDARD_SECTIONS, TUBE_DIAMETERS, LANG, labels

class Circuit:
    def __init__(self, c_type, desc, points: int, length_m=0):
        self.c_type = c_type
        self.desc = desc
        self.points = points
        self.length = length_m

        base = REBT_CATALOG.get(c_type, [16, 2.5, 20, 99])
        self.amps = base[0]
        self.section = base[1]
        self.tube = base[2]
        self.max_pts = base[3]

        self._calculate_physics()

    def _calculate_physics(self):
        """Applies Ohm's Law and REBT voltage drop limits."""
        if self.length == 0: return
        max_dv_volts = 230 * (0.03 if self.c_type == "C1" else 0.05)
        required_s = (2 * self.length * self.amps) / (48 * max_dv_volts)

        if required_s > self.section:
            for std_s in STANDARD_SECTIONS:
                if std_s >= required_s:
                    self.section = std_s
                    break
            self.tube = TUBE_DIAMETERS.get(self.section, self.tube)

    def __str__(self):
        warn = " [! EXCEDE PUNTOS]" if self.points > self.max_pts else ""
        len_str = f" ({labels['len']}{self.length}m)" if self.length > 0 else ""
        return (f"{self.c_type} - {self.desc}: PIA {self.amps}A | "
                f"{labels['wire']} {self.section}mm2 | {labels['tube']} {self.tube}mm | "
                f"{self.points} {labels['pts']}{len_str}{warn}")