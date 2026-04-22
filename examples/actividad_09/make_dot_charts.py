# %% [markdown]
# # Graphviz Decision Plots
# Generates PDF decision trees for the Rules Engines.

#%% setup graphviz
import os
print(os.getcwd())
# import dotenv
# dotenv.load_dotenv()
print(os.environ['PATH'])
if os.getenv('GRAPHVIZ_DOT') is not None:
    print(f"GRAPHVIZ_DOT={os.environ['GRAPHVIZ_DOT']}")
print(os.getenv('GRAPHVIZ_HOME'))
print(os.getenv('GRAPHVIZ_LIBRARY_PATH'))
print(os.getenv('GRAPHVIZ_DLL_PATH'))


# %%
import graphviz
import uuid

def generate_decision_plot(root_node, filename, title_en, title_es, lang='ES'):
    """
    Recursively traverses a RuleNode structure and generates a Graphviz plot.
    """
    # Initialize the directed graph
    dot = graphviz.Digraph(comment='Decision Engine', format='pdf')
    dot.attr(rankdir='TB', size='8,5')  # Top to Bottom layout
    dot.attr('node', fontname='Helvetica', shape='box', style='rounded,filled', fillcolor='#f9f9f9')

    # Set Bilingual Title
    title = title_es if lang == 'ES' else title_en
    dot.attr(label=f'\n{title}', labelloc='t', fontsize='16', fontname='Helvetica-Bold')

    def traverse(node, parent_id=None, edge_label=""):
        # Generate a unique ID for the Graphviz node
        node_id = str(uuid.uuid4())

        if hasattr(node, 'predicate'):
            # It's a RuleNode (Condition)
            # Use a diamond shape for decisions
            dot.node(node_id, node.name, shape='diamond', fillcolor='#fff2cc', style='filled')

            if parent_id:
                dot.edge(parent_id, node_id, label=edge_label, fontname='Helvetica', fontsize='10')

            # Recurse down the True and False paths
            traverse(node.on_true, node_id, "SÍ" if lang == 'ES' else "YES")
            traverse(node.on_false, node_id, "NO" if lang == 'ES' else "NO")

        else:
            # It's a Leaf (Final Result)
            # Use a bold box for conclusions
            dot.node(node_id, str(node), shape='box', fillcolor='#d5e8d4', style='filled,bold')

            if parent_id:
                dot.edge(parent_id, node_id, label=edge_label, fontname='Helvetica', fontsize='10', color='#666666')

    # Start the traversal from the root
    traverse(root_node)

    # Render and save the file
    dot.render(filename, view=False, cleanup=False)
    print(f"[{lang}] Guardado / Saved: {filename}.pdf")

    return dot


# %% Generate the plot for the Spatial / Type Engine
# Language toggle switch
LANG = 'ES'

plot_type = generate_decision_plot(
    root_node=type_node,
    filename="pdf/decision_tree_tipo_instalacion",
    title_en="Spatial Decision Engine: Installation Type",
    title_es="Motor de Decisión Espacial: Tipo de Instalación",
    lang=LANG
)


# Generate the plot for the Electrical / IGM Engine
plot_igm = generate_decision_plot(
    root_node=igm_node,
    filename="pdf/decision_tree_igm",
    title_en="Electrical Decision Engine: IGM Rating",
    title_es="Motor de Decisión Eléctrica: Calibre IGM",
    lang=LANG
)

# %%
# If you are running this inside a Jupyter Notebook,
# calling the object directly will display the SVG inline:
plot_type