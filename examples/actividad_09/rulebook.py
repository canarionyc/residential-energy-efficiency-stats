# %% Rule Engine and Rule Node
class RuleNode:
    def __init__(self, name, predicate, on_true, on_false):
        self.name = name
        self.predicate = predicate
        self.on_true = on_true
        self.on_false = on_false


class RuleEngine:
    def __init__(self, root_node):
        self.root = root_node
        self.is_primed = False

    def fireup_test(self):
        """
        Primer test: Validates the integrity of the DAG.
        Checks for dead ends or malformed nodes before processing data.
        """
        print("--- INICIANDO PRUEBA DE ARRANQUE (PRIMER) ---")
        visited = set()

        def check_node(node):
            if not isinstance(node, RuleNode):
                return  # Leaf reached
            if node in visited:
                raise Exception(f"Error: Ciclo detectado en {node.name}")
            visited.add(node)
            check_node(node.on_true)
            check_node(node.on_false)

        try:
            check_node(self.root)
            self.is_primed = True
            print("ESTADO: Motor de reglas certificado y listo.\n")
        except Exception as e:
            print(f"FALLO EN EL PRIMER: {e}")

    def run(self, context):
        if not self.is_primed:
            raise Exception("El motor debe ser 'primed' antes de la ejecución.")

        history = []
        current = self.root

        while isinstance(current, RuleNode):
            # We record only the dynamic data evaluation
            result = current.predicate(context)
            choice = "SÍ" if result else "NO"
            history.append(f"{current.name} -> {choice}")

            current = current.on_true if result else current.on_false

        return {"result": current, "history": history}