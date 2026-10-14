"""Rebuild the retail analytics tables from the official UCI Online Retail II workbook.

The deployed site already includes attributed aggregate extracts. This optional pipeline
recomputes them from the public workbook when network access is available.
Dependencies: pandas, numpy, openpyxl.
"""
from __future__ import annotations
from pathlib import Path
import json
import sqlite3
import urllib.request
import zipfile
import io
import shutil
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "aggregate"
PBI = ROOT / "powerbi_data"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
PBI.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)
UCI_ZIP = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
LOCAL = RAW / "online_retail_II.xlsx"


def fetch_workbook() -> None:
    if LOCAL.exists() and LOCAL.stat().st_size > 1_000_000:
        return
    print("Fetching official UCI Online Retail II workbook…")
    with urllib.request.urlopen(UCI_ZIP, timeout=180) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        candidates = [n for n in archive.namelist() if n.lower().endswith(".xlsx") and "online retail" in n.lower()]
        if not candidates:
            raise FileNotFoundError("No Online Retail II Excel workbook found inside the UCI archive.")
        LOCAL.write_bytes(archive.read(candidates[0]))


def export_csv(frame: pd.DataFrame, filename: str) -> None:
    frame.to_csv(OUT / filename, index=False, encoding="utf-8-sig")


def main() -> None:
    fetch_workbook()
    print("Reading workbook:", LOCAL)
    sheets = pd.read_excel(LOCAL, sheet_name=None, engine="openpyxl")
    raw = pd.concat(sheets.values(), ignore_index=True)
    raw_rows = int(len(raw))
    raw.columns = [str(c).strip().lower().replace(" ", "_") for c in raw.columns]
    alias = {
        "invoice": "invoice", "invoiceno": "invoice", "stockcode": "stock_code",
        "description": "description", "quantity": "quantity", "invoicedate": "invoice_date",
        "price": "unit_price", "unitprice": "unit_price", "customer_id": "customer_id",
        "customerid": "customer_id", "country": "country",
    }
    raw = raw.rename(columns={col: alias.get(col.replace("_", ""), alias.get(col, col)) for col in raw.columns})
    required = {"invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing expected columns {missing}; found {list(raw.columns)}")

    raw["invoice"] = raw["invoice"].astype(str).str.strip()
    raw["invoice_date"] = pd.to_datetime(raw["invoice_date"], errors="coerce")
    raw["quantity"] = pd.to_numeric(raw["quantity"], errors="coerce")
    raw["unit_price"] = pd.to_numeric(raw["unit_price"], errors="coerce")
    raw["customer_id"] = raw["customer_id"].apply(lambda x: None if pd.isna(x) else str(int(float(x))))
    before_dedupe = int(len(raw))
    data = raw.drop_duplicates().dropna(subset=["invoice_date", "quantity", "unit_price", "invoice"] ).copy()
    exact_duplicates_removed = before_dedupe - int(len(data))

    is_cancel = data["invoice"].str.upper().str.startswith("C") | (data["quantity"] < 0)
    returns = data[is_cancel & data["unit_price"].gt(0)].copy()
    returns["return_value_gbp"] = returns["quantity"].abs() * returns["unit_price"]
    sales = data[(~is_cancel) & data["quantity"].gt(0) & data["unit_price"].gt(0)].copy()
    sales["revenue_gbp"] = sales["quantity"] * sales["unit_price"]
    sales["month"] = sales["invoice_date"].dt.strftime("%Y-%m")
    returns["month"] = returns["invoice_date"].dt.strftime("%Y-%m")

    # Monthly revenue & invoices
    monthly = sales.groupby("month").agg(revenue_gbp=("revenue_gbp", "sum"), invoices=("invoice", "nunique")).reset_index()
    monthly["mom_growth_pct"] = monthly["revenue_gbp"].pct_change() * 100
    monthly["mom_growth_pct"] = monthly["mom_growth_pct"].round(1)
    export_csv(monthly, "monthly_revenue.csv")

    # Country mix
    country = sales.groupby("country", dropna=False)["revenue_gbp"].sum().sort_values(ascending=False).rename("revenue_gbp").reset_index()
    country["pct_of_total"] = 100 * country["revenue_gbp"] / country["revenue_gbp"].sum()
    country["pct_of_total"] = country["pct_of_total"].round(2)
    export_csv(country, "country_revenue.csv")

    # Top products
    products = sales.groupby("stock_code").agg(description=("description", "first"), units_sold=("quantity", "sum"), revenue_gbp=("revenue_gbp", "sum")).reset_index()
    products = products.sort_values("revenue_gbp", ascending=False).head(20)
    products["revenue_gbp"] = products["revenue_gbp"].round(2)
    export_csv(products, "top_products.csv")

    # Returns as value / same-month sales value
    monthly_returns = sales.groupby("month", as_index=False)["revenue_gbp"].sum().rename(columns={"revenue_gbp": "sales_gbp"})
    monthly_returns = monthly_returns.merge(returns.groupby("month", as_index=False)["return_value_gbp"].sum().rename(columns={"return_value_gbp": "returns_gbp"}), how="left", on="month").fillna({"returns_gbp": 0})
    monthly_returns["return_rate_pct"] = (100 * monthly_returns["returns_gbp"] / monthly_returns["sales_gbp"]).round(2)
    monthly_returns[["sales_gbp", "returns_gbp"]] = monthly_returns[["sales_gbp", "returns_gbp"]].round(2)
    export_csv(monthly_returns, "monthly_returns.csv")

    # RFM-style segmentation; this fresh run may differ from the shipped, attributed extract.
    customer = sales.dropna(subset=["customer_id"]).groupby("customer_id").agg(last_order=("invoice_date", "max"), frequency=("invoice", "nunique"), revenue_gbp=("revenue_gbp", "sum")).reset_index()
    snapshot = sales["invoice_date"].max() + pd.Timedelta(days=1)
    customer["recency_days"] = (snapshot - customer["last_order"]).dt.days
    customer["r_score"] = 6 - pd.qcut(customer["recency_days"].rank(method="first"), 5, labels=False).astype(int)
    customer["f_score"] = pd.qcut(customer["frequency"].rank(method="first"), 5, labels=False).astype(int) + 1
    cond = [
        (customer.r_score >= 4) & (customer.f_score >= 4),
        (customer.r_score >= 3) & (customer.f_score >= 3),
        (customer.r_score >= 4) & (customer.f_score <= 2),
        (customer.r_score >= 3) & (customer.f_score <= 2),
        (customer.r_score <= 2) & (customer.f_score >= 3),
        (customer.r_score <= 2) & (customer.f_score >= 2),
    ]
    names = ["Champions", "Loyal Customers", "New / Potential Loyalists", "Promising", "At Risk", "Hibernating"]
    customer["segment"] = np.select(cond, names, default="Lost")
    rfm = customer.groupby("segment").agg(customers=("customer_id", "count"), revenue_gbp=("revenue_gbp", "sum")).reset_index()
    rfm["pct_customers"] = (100 * rfm.customers / rfm.customers.sum()).round(1)
    rfm["pct_revenue"] = (100 * rfm.revenue_gbp / rfm.revenue_gbp.sum()).round(1)
    rfm["revenue_gbp"] = rfm["revenue_gbp"].round(2)
    export_csv(rfm.sort_values("revenue_gbp", ascending=False), "rfm_segments.csv")

    # Month-1 cohort retention
    sc = sales.dropna(subset=["customer_id"])[["customer_id", "month"]].drop_duplicates()
    first = sc.groupby("customer_id")["month"].min().rename("cohort_month").reset_index()
    joined = sc.merge(first, on="customer_id")
    sizes = joined[joined["month"] == joined["cohort_month"]].groupby("cohort_month")["customer_id"].nunique()
    cohort_rows = []
    for cohort, group in joined.groupby("cohort_month"):
        next_month = (pd.Period(cohort, "M") + 1).strftime("%Y-%m")
        cohort_size = int(sizes.get(cohort, 0))
        active = int(group.loc[group["month"] == next_month, "customer_id"].nunique())
        cohort_rows.append({"cohort_month": cohort, "cohort_size": cohort_size, "active_customers_month1": active, "retention_pct": round(100 * active / cohort_size, 1) if cohort_size else 0})
    cohort = pd.DataFrame(cohort_rows)
    export_csv(cohort, "cohort_month1_retention.csv")

    # Write Power BI CSVs to align them with freshly rebuilt extracts.
    mapping = {"monthly_revenue.csv": "MonthlyRevenue.csv", "country_revenue.csv": "CountryRevenue.csv", "top_products.csv": "TopProducts.csv", "monthly_returns.csv": "MonthlyReturns.csv", "rfm_segments.csv": "RFMSegments.csv", "cohort_month1_retention.csv": "CohortMonth1Retention.csv"}
    for src, dst in mapping.items(): shutil.copyfile(OUT / src, PBI / dst)

    # SQLite database used by the SQL scripts.
    db_path = PROCESSED / "online_retail_II.sqlite"
    if db_path.exists(): db_path.unlink()
    sales_db = sales.copy(); returns_db = returns.copy()
    for fr in (sales_db, returns_db):
        fr["invoice_date"] = fr["invoice_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_path) as con:
        sales_db[["invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country", "revenue_gbp"]].to_sql("sales", con, index=False)
        returns_db[["invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country", "return_value_gbp"]].to_sql("returns", con, index=False)
        con.execute("CREATE INDEX idx_sales_date ON sales(invoice_date)")
        con.execute("CREATE INDEX idx_sales_customer ON sales(customer_id)")

    # Dashboard payload (recomputed values; explicitly update static site payload only on request).
    revenue = float(sales["revenue_gbp"].sum())
    invoice_count = int(sales["invoice"].nunique())
    customer_count = int(sales["customer_id"].nunique())
    product_count = int(sales["stock_code"].nunique())
    country_count = int(sales["country"].nunique())
    payload = {
        "meta": {"title": "Retail Sales & Customer Analytics", "dataset": "UCI Online Retail II", "source_url": "https://archive.ics.uci.edu/dataset/502/online+retail+ii", "citation": "Chen, D. (2019). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.", "license": "CC BY 4.0", "published_aggregate_source": "https://github.com/ndkn-code/online-retail-analytics", "provenance_note": "Generated locally from the official UCI workbook using the included pipeline. Cleaning rules differ from the shipped aggregate extracts; inspect the quality report before comparing.", "period": f"{sales.invoice_date.min():%Y-%m-%d} to {sales.invoice_date.max():%Y-%m-%d}", "currency": "GBP (£)", "limitations": ["Historic data, not current business performance.", "RFM and cohort analysis require identified customers.", "The final observed month may be partial."]},
        "kpis": {"revenue_gbp": round(revenue, 2), "orders": invoice_count, "customers": customer_count, "products": product_count, "countries": country_count, "avg_order_value_gbp": round(revenue / invoice_count, 2) if invoice_count else 0, "clean_sales_lines": int(len(sales)), "raw_rows": raw_rows, "return_revenue_gbp": round(float(returns.return_value_gbp.sum()), 2), "return_revenue_pct": round(100 * float(returns.return_value_gbp.sum()) / revenue, 2) if revenue else 0, "period_start": f"{sales.invoice_date.min():%Y-%m-%d}", "period_end": f"{sales.invoice_date.max():%Y-%m-%d}"},
        "monthly": [{"month": str(r.month), "revenue_gbp": round(float(r.revenue_gbp), 2), "orders": int(r.invoices), "mom_growth_pct": None if pd.isna(r.mom_growth_pct) else float(r.mom_growth_pct)} for r in monthly.itertuples()],
        "countries": country.to_dict("records"),
        "products": [{"stock_code": str(r.stock_code), "product": str(r.description), "units_sold": int(r.units_sold), "revenue_gbp": round(float(r.revenue_gbp), 2)} for r in products.itertuples()],
        "returns": monthly_returns.to_dict("records"),
        "rfm": [{"segment": str(r.segment), "customers": int(r.customers), "pct_customers": float(r.pct_customers), "revenue_gbp": float(r.revenue_gbp), "pct_revenue": float(r.pct_revenue)} for r in rfm.itertuples()],
        "cohorts_month1": [{"cohort_month": str(r.cohort_month), "cohort_size": int(r.cohort_size), "active_customers_month1": int(r.active_customers_month1), "retention_pct": float(r.retention_pct)} for r in cohort.itertuples()],
    }
    # Make nan/null JSON-safe; then write the website payload.
    def clean_nan(obj):
        if isinstance(obj, dict): return {k: clean_nan(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_nan(v) for v in obj]
        if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)): return None
        return obj
    (ROOT / "data" / "dashboard_data.json").write_text(json.dumps(clean_nan(payload), indent=2, ensure_ascii=False), encoding="utf-8")

    quality = {
        "raw_rows": raw_rows,
        "rows_after_deduplication_and_required_field_validation": int(len(data)),
        "exact_duplicates_removed": exact_duplicates_removed,
        "positive_sales_lines": int(len(sales)),
        "returns_or_cancellation_lines": int(len(returns)),
        "sales_lines_missing_customer_id": int(sales.customer_id.isna().sum()),
        "identified_customers": customer_count,
        "distinct_invoices": invoice_count,
        "distinct_products": product_count,
        "distinct_countries": country_count,
        "revenue_gbp": round(revenue, 2),
        "return_value_gbp": round(float(returns.return_value_gbp.sum()), 2),
        "min_invoice_date": f"{sales.invoice_date.min():%Y-%m-%d}",
        "max_invoice_date": f"{sales.invoice_date.max():%Y-%m-%d}",
        "cleaning_note": "Fresh outputs are generated under the cleaning rules in this file and may not match the originally shipped, attributed aggregate extracts.",
    }
    (PROCESSED / "data_quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    print("\nRebuild complete")
    print(json.dumps(quality, indent=2))
    print("\nReview outputs and provenance before publishing regenerated results.")

if __name__ == "__main__":
    main()
