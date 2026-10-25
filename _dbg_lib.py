import sqlite3, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
try:
    rows = c.execute("SELECT id, filename, original_name, project_id, is_contract, uploader FROM library_files ORDER BY id DESC LIMIT 25").fetchall()
    for r in rows:
        print(r["id"], "|", r["original_name"], "| pid=", r["project_id"], "| contract=", r["is_contract"], "|", r["uploader"])
except Exception as e:
    print("ERR", e)
c.close()
