**Block 1: Project setup**

mkdir invoice-dispute-agent && cd invoice-dispute-agent

python -m venv .venv

source .venv/bin/activate # Windows: .venv\\Scripts\\activate

git init

mkdir generator matcher config tests data

A virtual environment keeps this project’s packages separate from everything else on your machine.

invoice-dispute-agent/

├── [README.md](http://README.md)                  # Main README (project, status, how to run, results)

├── .gitignore                 # .venv/, **pycache**/, data/

├── requirements.txt           # Python packages

├── Makefile                   # make data / make test / make eval

├── docs/

│   ├── [stage-1-design.md](http://stage-1-design.md)      # Your Stage 1 file

│   ├── [stage-2-data-and-matcher.md](http://stage-2-data-and-matcher.md)

│   └── assets/                # Diagram PNGs

├── config/

│   └── rules.yaml             # Tolerances, $2,000 threshold, precedence (Stage 2)

├── invoice_agent/             # All the project's Python code

│   ├── **init**.py

│   ├── common/                # Stage 2

│   │   ├── [money.py](http://money.py)           #   Decimal helpers

│   │   ├── [models.py](http://models.py)          #   Pydantic: Invoice, PurchaseOrder, Receipt, MatchResult

│   │   └── [db.py](http://db.py)              #   SQLite schema and connection

│   ├── generator/             # Stage 2: fake data, error injection, PDFs

│   │   ├── seed\_[data.py](http://data.py)

│   │   ├── inject\_[errors.py](http://errors.py)

│   │   ├── render\_[pdf.py](http://pdf.py)

│   │   └── templates/         #   HTML invoice template

│   ├── matcher/               # Stage 2: the rules

│   │   ├── [config.py](http://config.py)          #   Loads rules.yaml

│   │   └── [match.py](http://match.py)           #   match(invoice, po, receipt, rules)

│   ├── rag/                   # Stage 3: contract clause retrieval

│   ├── agent/                 # Stage 4: extraction, LangGraph workflow, email drafting

│   └── api/                   # Stage 5: FastAPI, login and roles, audit log

├── contracts/                 # Stage 3: contract PDFs

├── frontend/                  # Stage 5: React review screens

├── evals/                     # Stage 2 onwards

│   ├── [evaluate.py](http://evaluate.py)            #   Runs all 100 invoices against the answer key

│   └── results/               #   Saved reports

├── tests/                     # pytest (Stage 2 onwards)

│   ├── test\_[money.py](http://money.py)

│   └── test\_[matcher.py](http://matcher.py)

├── data/                       # Generated: SQLite file and PDFs (not committed)

├── Dockerfile                 # Stage 6

└── docker-compose.yml         # Stage 6

**Each folder has one job:**

`generator` makes fake data,

`matcher` holds the rules code,

`config` holds the YAML,

`tests` holds pytest,

`data` holds the database and PDFs.

### Block 2: `Decimal` for money (60 min)

**The problem.** Computers store floats in binary, and binary can’t represent 0.1 exactly:

\# float (Base-2 approximation)

print(0.1 + 0.2)

\# Output: 0.30000000000000004

print(0.1 + 0.2 == 0.3)

\# Output: False

from decimal import Decimal

\# Decimal (Base-10 exact representation)

print(Decimal('0.1') + Decimal('0.2'))

\# Output: 0.3

print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))

\# Output: True

***<u>Three rules to learn:</u>***

1. **Build** `Decimal` **from strings, never from floats.** `Decimal(0.1)` copies the float’s error.
2. **Round with** `quantize`**:** `Decimal("20.0449").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` gives `20.04`.
3. **Compare with** `Decimal`**, not float:** `abs(Decimal("20.04") - Decimal("20.00")) <= Decimal("0.05")` is `True`.

### Block 3: SQLite basics (75 min)

A SQLite database is one file. It holds **tables**; a table has **columns** (fields) and **rows** (records). You talk to it with SQL through Python’s built-in `sqlite3`.

import sqlite3

conn = sqlite3.connect("data/scratch.db")

conn.execute("""CREATE TABLE IF NOT EXISTS suppliers (

```
supplier_id INTEGER PRIMARY KEY,

name TEXT NOT NULL,

payment_terms TEXT)""")
```

conn.execute("INSERT INTO suppliers (name, payment_terms) VALUES (?, ?)",

```
         ("Sweet Co", "net 30"))
```

conn.commit()

rows = conn.execute("SELECT \* FROM suppliers WHERE name = ?", ("Sweet Co",)).fetchall()

Two things to notice:

- `PRIMARY KEY` is the unique id of each row.
- **Always use** `?` **placeholders**, never f-strings. Putting user text straight into SQL allows SQL injection, and interviewers like to ask about it.

For money columns today, use `INTEGER` cents (for example, 2004 for $20.04). We’ll settle the final storage choice on Day 2.

**Your exercise.** In `scratch_sql.py`:

1. Create the `suppliers` table.
2. Insert 3 suppliers.
3. Query one by name.
4. Count all rows with `SELECT COUNT(*)`.
5. `UPDATE` one supplier’s payment terms.
6. `DELETE` one supplier.

### Block 4: Wrap-up (15 min)

Commit your work with `git add . && git commit -m "Day 1: setup, money helpers, sqlite basics"`. Then say this answer out loud: **“Why not use floats for money?”** A good answer covers three points:

- Binary floats can’t represent most decimals exactly.
- Small errors break tolerance checks and add up across many invoices.
- You use `Decimal` built from strings, or integer cents.

<span style="color: rgb(229, 87, 87);">**<u>PYTHON TYPE HINTING</u>**</span>