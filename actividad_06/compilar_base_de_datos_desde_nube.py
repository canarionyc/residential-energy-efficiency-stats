# %% Cell: DuckDB Compilation from Google Sheets
import duckdb
import pandas as pd

# https://docs.google.com/spreadsheets/d/13VgjtU85yvMW02NLisRsmJ_LdGqg_h75oIn1sKe2Hks/edit?usp=sharing
def compilar_base_de_datos_desde_nube(db_path: str):
	# 1. Configuration: Replace with your actual IDs
	SHEET_ID = "13VgjtU85yvMW02NLisRsmJ_LdGqg_h75oIn1sKe2Hks"

	# Replace these with the actual GIDs from your tabs
	GID_METODOS = "0"  # Usually 0 for the first tab
	GID_INTENSIDADES = "1410229836"  # Click your second tab and copy the GID from the URL

	# Construct the direct download URLs
	url_metodos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_METODOS}"
	url_intensidades = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_INTENSIDADES}"

	print("Fetching normative tables from Google Cloud...")

	# 2. Read directly into Pandas DataFrames
	try:
		df_metodos = pd.read_csv(url_metodos)
		df_intensidades = pd.read_csv(url_intensidades)
		# Optional: Strip whitespace from column names just in case
		df_metodos.columns = df_metodos.columns.str.strip()
		df_intensidades.columns = df_intensidades.columns.str.strip()
	except Exception as e:
		print(f"❌ Failed to fetch data. Check if the sheet is public. Error: {e}")
		return

	# 3. Compile the local DuckDB database
	with duckdb.connect(db_path) as db:
		# Create strict tables
		db.execute("""
            CREATE TABLE IF NOT EXISTS metodos_instalacion (
                id_sistema VARCHAR PRIMARY KEY,
                descripcion VARCHAR
            );
        """)

		db.execute("""
            CREATE TABLE IF NOT EXISTS intensidades_admisibles (
                id_sistema VARCHAR,
                seccion_mm2 DOUBLE,
                material VARCHAR,
                intensidad_A DOUBLE,
                FOREIGN KEY (id_sistema) REFERENCES metodos_instalacion(id_sistema)
            );
        """)

		# Clear existing data in case you are re-running to update rules
		db.execute("DELETE FROM intensidades_admisibles")
		db.execute("DELETE FROM metodos_instalacion")

		# Insert fresh data from the cloud
		db.execute("INSERT INTO metodos_instalacion SELECT * FROM df_metodos")
		db.execute("INSERT INTO intensidades_admisibles SELECT * FROM df_intensidades")

	print(f"✅ DuckDB database successfully compiled at: {db_path}")

# Execute the compilation
compilar_base_de_datos_desde_nube('normativas.duckdb')