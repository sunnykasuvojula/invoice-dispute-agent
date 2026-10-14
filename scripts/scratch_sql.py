import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "scratch.db"
conn=sqlite3.connect(DB_PATH)
conn.execute("CREATE TABLE IF NOT EXISTS suppliers(" \
"supplier_id INTEGER PRIMARY KEY, " \
"name TEXT NOT NULL, " \
"payment_terms text)" \
"")

conn.execute("INSERT INTO suppliers(name,payment_terms) VALUES(?,?)",("Sweet Co","net 30"))

conn.execute("INSERT INTO suppliers(name,payment_terms) VALUES(?,?)",("Helix Co","net 150"))

conn.execute("INSERT INTO suppliers(name,payment_terms) VALUES(?,?)",("Gordan Co","net 85"))

conn.commit()
rows=conn.execute("SELECT * FROM suppliers WHERE name=?",("Sweet Co",)).fetchall()