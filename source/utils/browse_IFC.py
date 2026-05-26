import sys
import ifcopenshell
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

def populate_tree(parent_item, ifc_parent):
    """Recursively finds children and adds them to the PyQt6 tree."""
    # 1. Find elements connected by decomposition (e.g., Project -> Site -> Building -> Storey)
    if hasattr(ifc_parent, 'IsDecomposedBy'):
        for rel in ifc_parent.IsDecomposedBy:
            for child in rel.RelatedObjects:
                node_name = f"{child.is_a()} - {child.Name or 'Unnamed'}"
                child_item = QTreeWidgetItem(parent_item, [node_name])
                populate_tree(child_item, child) # Recurse deeper
            
    # 2. Find physical elements contained in this spatial structure (e.g., Storey -> Electrical Fixtures)
    if hasattr(ifc_parent, 'ContainsElements'):
        for rel in ifc_parent.ContainsElements:
            for element in rel.RelatedElements:
                node_name = f"{element.is_a()} - {element.Name or 'Unnamed'}"
                # We don't recurse here because physical elements are usually the "leaves" of the spatial tree
                QTreeWidgetItem(parent_item, [node_name])


class IFCBrowser(QMainWindow):
    def __init__(self, ifc_filepath):
        super().__init__()
        self.setWindowTitle("IFC Node Explorer (PyQt6)")
        self.resize(600, 800)

        # Setup the Tree Widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("IFC Spatial Hierarchy")
        self.setCentralWidget(self.tree)

        # Load data
        self.load_ifc(ifc_filepath)

    def load_ifc(self, filepath):
        try:
            model = ifcopenshell.open(filepath)
            
            # Find the root project element
            projects = model.by_type("IfcProject")
            if not projects:
                print("No IfcProject found in the file.")
                return
            
            project = projects[0]

            # Create the root node in the GUI
            root_name = f"{project.is_a()} - {project.Name or 'Unnamed Project'}"
            root_item = QTreeWidgetItem(self.tree, [root_name])
            
            # Start the recursive population
            populate_tree(root_item, project)
            
            # Expand the root node by default
            root_item.setExpanded(True)
            
        except Exception as e:
            print(f"Error loading IFC file: {e}")

# --- Run the application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ifc_file_path = r"/examples/ifc4_all/Unifamiliar/Unifamiliar.ifc"
    # Replace 'your_cype_model.ifc' with the actual path to your file
    window = IFCBrowser(ifc_file_path)
    window.show()
    
    sys.exit(app.exec())