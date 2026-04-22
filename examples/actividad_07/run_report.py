import os
import json
import jinja2

# 1. Reconfigure Jinja2 for LaTeX compatibility
latex_jinja_env = jinja2.Environment(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='<<',
    variable_end_string='>>',
    comment_start_string='<#',
    comment_end_string='#>',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))  # Looks in current folder
)


def generar_latex(resultados: list, nombre_salida: str = "informe_final.tex"):
    # 2. Load the template
    template = latex_jinja_env.get_template('plantilla_informe.tex')

    # 3. Render the template with the JSON data
    latex_compilado = template.render(resultados=resultados)

    # 4. Save to file
    with open(nombre_salida, 'w', encoding='utf-8') as f:
        f.write(latex_compilado)

    print(f"✅ Documento LaTeX generado exitosamente: {nombre_salida}")

# Trigger the generation
resultados=json.load(open('resultados.json', 'r'))
generar_latex(resultados=resultados)