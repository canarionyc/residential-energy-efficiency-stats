from circuit import Circuit

class RCDGroup:
    def __init__(self, rcd_id: str):
        self.rcd_id = rcd_id
        self.circuits = []

    def add(self, circuit : Circuit):
        self.circuits.append(circuit)