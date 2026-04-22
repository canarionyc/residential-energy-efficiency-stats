import duckdb

# Create an in-memory database (or connect to a file like 'normas.db')
db = duckdb.connect(r'normas.db')

# Let's simulate ingesting a table of installation systems from the UNE-HD 60364-5-52
db.execute("""
    CREATE TABLE metodos_instalacion (
        id VARCHAR PRIMARY KEY,.
        descripcion VARCHAR
    );
    INSERT INTO metodos_instalacion VALUES 
        ('A1', 'Conductores aislados en tubos en paredes aislantes'),
        ('B1', 'Conductores aislados en tubos sobre pared de madera o mampostería'),
        ('C', 'Cables multiconductores sobre pared de madera o mampostería');
""")

db.close()