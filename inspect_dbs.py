import os
print(os.getcwd())

from pprint import pprint
import duckdb
from pathlib import Path

def inspect_duckdb_files(search_directory="."):
    root_path = Path(search_directory)
    # Recursively find all files ending in .duckdb
    duckdb_files = list(root_path.rglob("*.duckdb"))
    
    if not duckdb_files:
        print(f"No .duckdb files found in '{root_path.resolve()}'")
        return

    print(f"Found {len(duckdb_files)} DuckDB database(s). Scanning...\n")

    for db_path in duckdb_files:
        print("=" * 60)
        print(f"DATABASE: {db_path.name}")
        print(f"PATH:     {db_path.resolve()}")
        print("=" * 60)
        
        try:
            # Open in read_only mode so it doesn't lock active databases
            conn = duckdb.connect(database=str(db_path), read_only=True)
            
            # Fetch all user-defined tables
            tables = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            """).fetchall()
            
            if not tables:
                print("  (No tables found in this database)\n")
                conn.close()
                continue
                
            for (table_name,) in tables:
                print(f"\n  [Table] {table_name}")
                
                # Get Row Count
                row_count = conn.execute(f"SELECT COUNT(*) FROM \"{table_name}\"").fetchone()[0]
                print(f"  ├── Occupation: {row_count:,} rows")
                
                # Get Columns and Types
                print("  └── Schema:")
                columns = conn.execute(f"PRAGMA table_info(\"{table_name}\")").fetchall()
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    print(f"      ├── {col_name} ({col_type})")
                    
            conn.close()
        except Exception as e:
            print(f"  ❌ Error reading database: {e}")
        print("\n")

if __name__ == "__main__":
    # Change "." to a specific path if you want to scan a different directory
    inspect_duckdb_files(".")