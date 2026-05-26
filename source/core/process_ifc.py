#%% [IMPORT LIBRARIES]
import gc
import ifcopenshell
import json

#%% [IFC PROCESSOR CLASS]
class IFCProcessor:
    """
    A class to load and extract basic information from an IFC file.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.model = None

    def load_model(self):
        """Loads the IFC model using IfcOpenShell."""
        try:
            self.model = ifcopenshell.open(self.filepath)
            print(f"Successfully loaded {self.filepath}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def get_schema(self):
        """Returns the IFC schema version."""
        if self.model:
            return self.model.schema
        return None

    def plot_element_quantities(self, element_type="IfcWall", lang="EN"):
        """
        Mock method demonstrating bilingual plotting structures 
        for extracted IFC element quantities.
        """
        # Bilingual plot configuration dictionary
        plot_config = {
            "title": "Quantity of Elements",
            "x_axis": "Element Type",
            "y_axis": "Count",
            "annotations": "Data extracted via IfcOpenShell"
        }
        
        if lang == "ES":
            plot_config.update({
                "title": "Cantidad de Elementos",
                "x_axis": "Tipo de Elemento",
                "y_axis": "Conteo",
                "annotations": "Datos extraídos mediante IfcOpenShell"
            })
            
        print(f"Plot Configuration Setup:\n{json.dumps(plot_config, indent=4)}")
        # Plotting logic would go here

    def close_model(self):
        """Release the IFC model before interpreter shutdown."""
        self.model = None
        gc.collect()

#%% [DEMONSTRATION]
if __name__ == "__main__":
    import os
    # Basic demonstration of the functionality
    # Note: You will need a complete .ifc file to load successfully.
    ifc_file_path = r"/examples/ifc4/Unifamiliar/Unifamiliar.ifc"
    if not os.path.exists(ifc_file_path):
        print(f"IFC file not found at {ifc_file_path}. Please update the path to a valid IFC file.")
        exit(1)
    
    processor = IFCProcessor(ifc_file_path)

    try:
        if processor.load_model():
            print(f"Schema: {processor.get_schema()}")
            processor.plot_element_quantities(lang="ES")
    finally:
        processor.close_model()