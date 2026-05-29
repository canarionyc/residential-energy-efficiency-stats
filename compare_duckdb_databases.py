import duckdb
import shutil
import sys
from pathlib import Path

try:
    from tkinter import filedialog
    import tkinter as tk
    GUI_AVAILABLE = True
except ImportError:
    filedialog = None
    tk = None
    GUI_AVAILABLE = False

def format_schema_tree(schema_tuples):
    """Format schema tuples as a hierarchical tree structure.

    Input: List of (table_name, column_name, column_type) tuples
    Output: Formatted string showing schema as tree
    """
    if not schema_tuples:
        return "  (empty)"

    # Group by table
    tables = {}
    for table_name, col_name, col_type in schema_tuples:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append((col_name, col_type))

    # Format as tree
    lines = []
    sorted_tables = sorted(tables.keys())
    for i, table_name in enumerate(sorted_tables):
        is_last_table = (i == len(sorted_tables) - 1)
        table_prefix = "└── " if is_last_table else "├── "
        lines.append(f"  {table_prefix}📋 {table_name}")

        columns = sorted(tables[table_name])
        for j, (col_name, col_type) in enumerate(columns):
            is_last_col = (j == len(columns) - 1)
            col_prefix = "    └── " if is_last_col else "    ├── "
            lines.append(f"{col_prefix}{col_name}: {col_type}")

    return "\n".join(lines)


def format_schema_diff_tree(tuples_unique_db1, tuples_unique_db2):
    """Format schema differences side-by-side in tree format."""
    output = []

    if tuples_unique_db1:
        output.append("  ❌ Elements unique to DB1:")
        output.append(format_schema_tree(tuples_unique_db1))

    if tuples_unique_db2:
        output.append("  ❌ Elements unique to DB2:")
        output.append(format_schema_tree(tuples_unique_db2))

    return "\n".join(output)


def create_merged_database(db1_path, db2_path, merged_path=None):
    """Create a merged database by duplicating db1 and copying db2 tables into it."""
    p1, p2 = Path(db1_path), Path(db2_path)
    merged_path = Path(merged_path) if merged_path else p1.with_name("merged.duckdb")

    if merged_path.exists():
        merged_path.unlink()

    shutil.copy2(p1, merged_path)

    merged_con = duckdb.connect(str(merged_path))
    source_con = duckdb.connect(str(p2), read_only=True)
    try:
        merged_con.execute(f"ATTACH '{p2}' AS src (READ_ONLY);")
        source_tables = source_con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='main' ORDER BY table_name"
        ).fetchall()

        copied_tables = []
        for (table_name,) in source_tables:
            merged_con.execute(f'CREATE TABLE main."{table_name}" AS SELECT * FROM src.main."{table_name}"')
            copied_tables.append(table_name)

        return merged_path, copied_tables
    finally:
        try:
            merged_con.execute("DETACH src;")
        except Exception:
            pass
        merged_con.close()
        source_con.close()

def compare_duckdb_databases(db1_path, db2_path):
    p1, p2 = Path(db1_path), Path(db2_path)
    if not p1.exists():
        print(f"❌ Error: {p1.resolve()} do not exist.")
        return
    if not p2.exists():
        print(f"❌ Error: {p2.resolve()} do not exist.")
        return

    print(f"Comparing:\n  [DB1] {p1.resolve()}\n  [DB2] {p2.resolve()}\n")

    # Connect to each database independently
    con1 = duckdb.connect(str(p1), read_only=True)
    con2 = duckdb.connect(str(p2), read_only=True)

    # 1. COMPARE SCHEMAS (Tables, Columns, Types)
    print("📋 Checking Schemas...")

    # Get schema from db1: list all tables and their columns
    db1_tables = con1.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
    db1_schema = []
    for (table_name,) in db1_tables:
        try:
            cols = con1.execute(f"DESCRIBE \"{table_name}\"").fetchall()
            for col_name, col_type, *rest in cols:
                db1_schema.append((table_name, col_name, col_type))
        except Exception as e:
            print(f"  ⚠️  Warning: Could not describe table '{table_name}' in DB1: {e}")

    # Get schema from db2: list all tables and their columns
    db2_tables = con2.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
    db2_schema = []
    for (table_name,) in db2_tables:
        try:
            cols = con2.execute(f"DESCRIBE \"{table_name}\"").fetchall()
            for col_name, col_type, *rest in cols:
                db2_schema.append((table_name, col_name, col_type))
        except Exception as e:
            print(f"  ⚠️  Warning: Could not describe table '{table_name}' in DB2: {e}")

    # Find discrepancies using set differences
    set1 = set(db1_schema)
    set2 = set(db2_schema)

    schema_mismatch = False
    if set1 != set2:
        schema_mismatch = True
        print("❌ SCHEMA MISMATCH FOUND!\n")
        only_in_db1 = sorted(list(set1 - set2))
        only_in_db2 = sorted(list(set2 - set1))

        if only_in_db1 or only_in_db2:
            print(format_schema_diff_tree(only_in_db1, only_in_db2))
    else:
        print("✅ Schemas are perfectly identical.")

    # 2. COMPARE DATA 
    print("\n📊 Checking Data Rows...")
    # Get common tables to safely compare data
    db1_table_names = {row[0] for row in con1.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()}
    db2_table_names = {row[0] for row in con2.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()}
    common_tables = db1_table_names.intersection(db2_table_names)

    if not common_tables:
        print("❌ No common tables to compare data.")
        merged_path, copied_tables = create_merged_database(p1, p2)
        print(f"🧩 Created merged database: {merged_path.resolve()}")
        print(f"📦 Copied {len(copied_tables)} tables from DB2 into merged.duckdb")
        con1.close()
        con2.close()
        return

    data_mismatch_count = 0
    
    for table in common_tables:
        try:
            # Get row counts
            count1 = con1.execute(f"SELECT COUNT(*) FROM \"{table}\"").fetchone()[0]
            count2 = con2.execute(f"SELECT COUNT(*) FROM \"{table}\"").fetchone()[0]

            if count1 != count2:
                data_mismatch_count += 1
                print(f"  ❌ Table '{table}': FAILED (Row count mismatch: DB1={count1}, DB2={count2})")
            else:
                # Compare actual data by checking for row differences
                # Get data from both as pandas-compatible format
                try:
                    data1 = con1.execute(f"SELECT * FROM \"{table}\" ORDER BY rowid").fetchall()
                    data2 = con2.execute(f"SELECT * FROM \"{table}\" ORDER BY rowid").fetchall()

                    if data1 != data2:
                        data_mismatch_count += 1
                        print(f"  ❌ Table '{table}': FAILED (Data content mismatch)")
                    else:
                        print(f"  ✅ Table '{table}': PASSED (Data is identical)")
                except Exception as e:
                    print(f"  ⚠️  Table '{table}': Could not compare detailed content ({e})")
                    # Still mark as potentially mismatched
                    data_mismatch_count += 1
        except Exception as e:
            print(f"  ❌ Table '{table}': Could not evaluate ({e})")
            data_mismatch_count += 1

    con1.close()
    con2.close()

    print("\n" + "="*40)
    if schema_mismatch or data_mismatch_count > 0:
        print("🚨 VERIFICATION FAILED: The databases are different.")
    else:
        print("🎉 SUCCESS: Schemas and data match 100% perfectly!")
    print("="*40)

def select_file_gui(title: str, initial_dir: str | None = None) -> str | None:
    """Select a file using GUI if available, otherwise prompt via console."""
    if GUI_AVAILABLE:
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title=title,
            filetypes=[("DuckDB files", "*.duckdb"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        root.destroy()
        return path
    else:
        return None


def select_file_console(prompt):
    """Prompt user for a file path via console."""
    while True:
        path = input(prompt).strip()
        if not path:
            print("❌ Empty path provided.")
            continue
        p = Path(path)
        if not p.exists():
            print(f"❌ File not found: {path}")
            continue
        if not p.is_file():
            print(f"❌ Not a file: {path}")
            continue
        return str(p)


if __name__ == "__main__":
    # Usage: python script.py path/to/db1.duckdb path/to/db2.duckdb
    # Or: python script.py (opens file chooser dialog or console prompt)

    db1_path = None
    db2_path = None

    if len(sys.argv) >= 3:
        # Command-line arguments provided
        db1_path = sys.argv[1]
        db2_path = sys.argv[2]
    elif GUI_AVAILABLE:
        # Show GUI file chooser
        print("🖥️  Opening file chooser for database selection...")

        # Select first database
        db1_path = select_file_gui("Select first database (DB1)")

        if not db1_path:
            print("❌ No database selected. Exiting.")
            sys.exit(1)

        # Select second database
        db2_path = select_file_gui("Select second database (DB2)", initial_dir=str(Path(db1_path).parent))

        if not db2_path:
            print("❌ No database selected. Exiting.")
            sys.exit(1)
    else:
        # Fallback to console-based input
        print("📝 GUI not available. Please enter database paths manually.")
        db1_path = select_file_console("Enter path to first database (DB1): ")
        db2_path = select_file_console("Enter path to second database (DB2): ")

    compare_duckdb_databases(db1_path, db2_path)