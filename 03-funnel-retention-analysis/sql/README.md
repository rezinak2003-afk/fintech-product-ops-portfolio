# SQL Setup

## Option A — DB Browser for SQLite (GUI)
1. Install/open DB Browser for SQLite.
2. Create a new database named `funnel_retention.db`.
3. Open the Execute SQL tab and run `schema.sql`.
4. Import `../data/users.csv` into table `users` and `../data/events.csv` into table `events`, matching existing table names and columns. If importing creates new tables rather than filling the existing schema, delete/rename them and repeat with “append to existing table.”
5. Run `funnel_analysis.sql` and `retention_analysis.sql` and export the result sets as CSV.

## Option B — Python standard library
Run from this `sql` folder:

```bash
python import_and_run.py
```

This helper imports the source CSVs into a local SQLite database and executes the query files; no third-party Python packages are required.
