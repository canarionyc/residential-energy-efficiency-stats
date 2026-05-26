# %% [IMPORT LIBRARIES]
import ifcopenshell
import ifcopenshell.util.element as util
import json
from pprint import pprint
from core.process_ifc import IFCProcessor

# %% [ELECTRICAL EXTRACTOR CLASS]
class ElectricalPropertyExtractor(IFCProcessor):

    def extract_electrical_data(self):
        if not self.model:
            return []

        # Expanded list to catch IFC2x3 generics and IFC4 specifics
        target_classes = [
            "IfcElectricAppliance",  # IFC4 Specific
            "IfcLamp",  # IFC4 Specific
            "IfcSwitchingDevice",  # IFC4 Specific
            "IfcFlowTerminal",  # IFC2x3 Generic (Outlets/Lamps)
            "IfcEnergyConversionDevice",  # IFC2x3 Generic (Motors/Transformers)
            "IfcFlowController",  # IFC2x3 Generic (Switches)
            "IfcSolarDevice"
        ]

        extracted_elements = []

        for ifc_class in target_classes:
            print(f"Extracting properties for class: {ifc_class}")
            elements = self.model.by_type(ifc_class)
            print(f"Found {len(elements)} elements of class: {ifc_class}")
            for element in elements:
                print(f"Got element name {element.Name} with description {element.Description}")
                # Get instance properties
                psets = ifcopenshell.util.element.get_psets(element)
                print(f"Extracted {len(psets)} psets for {element.Name}:")
                pprint(psets)
                # IMPORTANT: In many models, properties are attached to the TYPE, not the instance
                if hasattr(element, "IsDefinedBy"):
                    type_psets = ifcopenshell.util.element.get_psets(element, psets_only=True)
                    psets.update(type_psets); pprint(type_psets)

                if psets:
                    extracted_elements.append({
                        "GlobalId": element.GlobalId,
                        "Name": element.Name or "Unnamed",
                        "Class": element.is_a(),
                        "Properties": psets
                    })

                # Extract spatial container hierarchy (Site -> Building -> Storey)
                container = util.get_container(element)
                print(f"Contained in {container.Name} with description {container.Description}")
                pprint(container)

        return extracted_elements

    def plot_electrical_summary(self, data, lang="EN"):
        counts = {}
        for item in data:
            cls = item["Class"]
            counts[cls] = counts.get(cls, 0) + 1

        plot_config = {
            "title": "Electrical Elements Summary",
            "x_axis": "Element Class",
            "y_axis": "Count",
            "annotations": "Electrical Psets extracted via ifcopenshell.util",
            "data_series": counts
        }

        if lang == "ES":
            plot_config.update({
                "title": "Resumen de Elementos Eléctricos",
                "x_axis": "Clase de Elemento",
                "y_axis": "Cantidad",
                "annotations": "Psets eléctricos extraídos mediante ifcopenshell.util"
            })

        # ensure_ascii=False handles the encoding for Spanish characters in the console
        print(f"Plot Configuration Setup:\n{json.dumps(plot_config, indent=4, ensure_ascii=False)}")

# %% [DEMONSTRATION]
if __name__ == "__main__":
    # Test with your new IFC4 file for better results
    ifc_file_path = r"/Bonsai/Unifamiliar_Ifc4.ifc"

    extractor = ElectricalPropertyExtractor(ifc_file_path)
    try:
        if extractor.load_model():
            electrical_data = extractor.extract_electrical_data()
            print(f"\nFound {len(electrical_data)} electrical elements.")

            if electrical_data:
                # Show properties of the first item found
                first_item = electrical_data[0]
                print(f"Sample Properties for {first_item['Name']}:")
                print(json.dumps(first_item['Properties'], indent=2, ensure_ascii=False))

            extractor.plot_electrical_summary(electrical_data, lang="ES")
    finally:
        extractor.close_model()