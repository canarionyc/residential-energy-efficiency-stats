#%%
import os
print(os.getcwd())
# %%

import duckdb

# Conectar a la base de datos existente
db_path = 'db/normativas.duckdb' # Ajusta la ruta si es necesario

with duckdb.connect(db_path) as db:
    # Esto creará una carpeta llamada 'backup_normativas' en tu directorio actual
    # Volcará el esquema en SQL y los datos en CSV
    db.execute("EXPORT DATABASE 'backup_normativas' (FORMAT CSV, HEADER 1);")

print("✅ Volcado completado en la carpeta 'backup_normativas'")