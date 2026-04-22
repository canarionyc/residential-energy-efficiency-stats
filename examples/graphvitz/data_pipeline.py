import graphviz

dot = graphviz.Digraph(comment='The Data Pipeline')
dot.node('A', 'Raw Data')
dot.node('B', 'Etl Process')
dot.node('C', 'Database')

dot.edges(['AB', 'BC'])
dot.render('pipeline-output', format='png', view=True)