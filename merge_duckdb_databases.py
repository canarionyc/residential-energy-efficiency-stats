import duckdb
import os
import sys
from pathlib import Path

def merge_duckdb_databases(db1_path, db2_path, output_path="merged.duckdb"):
    p1, p2, pout = Path(db1_path), Path(db2_path), Path(output_path)
    
    if not p1.exists() or not p2.exists():
        print("❌ Error: One or both source databases do not exist.")
        return

    # Start fresh: clear out any older merged file if present
    if pout.exists():
        os.remove(pout)
        
    print(f"🚀 Initializing merge into: {pout.resolve()}")
    
    # Open the new target database and attach the sources as read-only
    con = duckdb.connect(str(pout))
    con.execute(f"ATTACH '{p1}' AS src1 (READ_ONLY);")
    con.execute(f"ATTACH '{p2}' AS src2 (READ_ONLY);")
    
    # Inventory tables from both sources
    tables_db1 = [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables WHERE table_catalog='src1' AND table_schema='main'").fetchall()]
    tables_db2 = [r[0] for r in con.execute("SELECT table_name FROM information_schema.tables WHERE table_catalog='src2' AND table_schema='main'").fetchall()]
    
    set1, set2 = set(tables_db1), set(tables_db2)
    common_tables = set1.intersection(set2)
    unique_db1 = set1 - set2
    unique_db2 = set2 - set1
    
    # 1. Process Unique Tables from DB1 (Write directly to main schema)
    for table in unique_db1:
        print(f"  ├── ➡️ Moving unique table '{table}' (DB1) to main.{table}")
        con.execute(f"CREATE TABLE main.\"{table}\" AS SELECT * FROM src1.main.\"{table}\"")
        
    # 2. Process Unique Tables from DB2 (Write directly to main schema)
    for table in unique_db2:
        print(f"  ├── ➡️ Moving unique table '{table}' (DB2) to main.{table}")
        con.execute(f"CREATE TABLE main.\"{table}\" AS SELECT * FROM src2.main.\"{table}\"")
        
    # 3. Handle Overlapping Tables using custom schemas
    if common_tables:
        print(f"\n⚠️  Found {len(common_tables)} overlapping table name(s). Isolating namespaces...")
        con.execute("CREATE SCHEMA db1;")
        con.execute("CREATE SCHEMA db2;")
        
        for table in common_tables:
            print(f"  ├── 🔀 Resolving '{table}':")
            print(f"  │    ├── src1.{table} ➡️ db1.{table}")
            con.execute(f"CREATE TABLE db1.\"{table}\" AS SELECT * FROM src1.main.\"{table}\"")
            print(f"  │    └── src2.{table} ➡️ db2.{table}")
            con.execute(f"CREATE TABLE db2.\"{table}\" AS SELECT * FROM src2.main.\"{table}\"")
            
    # Clean up connections
    con.execute("DETACH src1;")
    con.execute("DETACH src2;")
    con.close()
    
    print("\n" + "="*50)
    print("🎉 SUCCESS: Databases merged seamlessly!")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_script.py <path_to_db1.duckdb> <path_to_db2.duckdb> [optional_output_name.duckdb]")
    else:
        out = sys.argv[3] if len(sys.argv) > 3 else "merged.duckdb"
        merge_duckdb_databases(sys.argv[1], sys.argv[2], out)