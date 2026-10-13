# Funnel & Retention Analysis

**Dataset:** `BNPL Funnel & Retention Synthetic Dataset v1` · **Population:** 5,000 simulated visitor IDs · **Events:** 37,097 synthetic event rows · **Window:** 2026-01-01 to 2026-09-30

## What is included
- `index.html`: interactive dashboard with device/region filters, funnel conversion, and weekly cohort retention.
- `data/users.csv`: one row per simulated visitor, including nullable signup date and device/region/channel.
- `data/events.csv`: synthetic timestamped event stream.
- `dashboard_data.json`: generated aggregates consumed by the static dashboard.
- `sql/schema.sql`, `sql/funnel_analysis.sql`, `sql/retention_analysis.sql`: SQLite-compatible analysis.
- `sql/power_bi_measures.md`: suggested DAX measures and a Power BI recreation guide.
- `data_dictionary.md`: field meanings and caveats.
- `generate_dashboard_data.py`: regenerate data and pre-aggregations deterministically.

## Results to discuss carefully
The data deliberately encodes differences in KYC submission probability by device and region so that the analysis demonstrates how to segment a funnel. Any observed ranking or drop-off in this package is a result of the **synthetic generation rules**, not an empirical business finding. The dashboard repeats that limitation visibly.

## Run locally
Run `python -m http.server 8000` from this directory and open `http://localhost:8000`. The dashboard fetches `dashboard_data.json`, so serve it over HTTP rather than opening the file directly. Python is needed only for this local server or for regenerating the data; the deployed dashboard is static.

## Run SQL in SQLite
Create a database and import CSVs. See `sql/README.md` for step-by-step commands. SQLite Desktop tools such as DB Browser for SQLite can also import both CSVs.

## Deployment
See root `DEPLOYMENT_GUIDE.md`.
