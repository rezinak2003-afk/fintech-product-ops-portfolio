# Power BI report build guide

## 1. Generate data first
Run `RUN_PIPELINE.bat`. It creates CSVs under `powerbi_data/`. The `fact_sales.csv` table contains eligible positive purchase lines; `cancellations.csv` is separate to avoid counting cancellations as positive sales.

## 2. Import these tables
Power BI Desktop → **Get data → Text/CSV**:
- `fact_sales.csv`
- `dim_customer.csv`
- `dim_product.csv`
- `dim_date.csv`
- `monthly_cohort_retention.csv`
- `cancellations_monthly.csv`

Set `fact_sales[invoice_date]` and `dim_date[date]` to Date/DateTime types; set `customer_id`, `invoice_no`, and `stock_code` to Text (IDs are categorical, not measures). `line_revenue` should be Decimal Number. Set report currency to GBP.

## 3. Model relationships
- `dim_date[date]` (1) → `fact_sales[invoice_date_date]` (*) — both columns are date-only `YYYY-MM-DD` values. Set both to Date type.
- `dim_customer[customer_id]` (1) → `fact_sales[customer_id]` (*) — single direction. Blank IDs will not match a customer dimension row.
- `dim_product[stock_code]` (1) → `fact_sales[stock_code]` (*) — ensure product dimension has one row per stock code. If descriptions vary by code across time, deduplicate in Power Query by stock_code or keep a combined product key.

`monthly_cohort_retention.csv` is a pre-aggregated cohort fact table; use it directly for a cohort matrix. It does not need a relationship to fact_sales for the supplied cohort visuals.

## 4. DAX measures
Create these measures on `fact_sales`:

```DAX
Revenue GBP = SUM(fact_sales[line_revenue])
Orders = DISTINCTCOUNT(fact_sales[invoice_no])
Units Sold = SUM(fact_sales[quantity])
Known Customers = DISTINCTCOUNT(fact_sales[customer_id])
Average Order Value GBP = DIVIDE([Revenue GBP], [Orders])
Sales Lines = COUNTROWS(fact_sales)
```

For customer counts, blanks may be counted inconsistently depending on DAX expression/context. If needed, use a filtered measure:

```DAX
Known Customers (nonblank) =
CALCULATE(
    DISTINCTCOUNT(fact_sales[customer_id]),
    fact_sales[customer_id] <> BLANK()
)
```

For monthly-cohort matrix, use `cohort_month` as rows, `month_index` as columns, and `retention_rate` as values (format as percentage). Do not average rates across cohorts without weighting; present each cohort row independently. Add `active_customers` and `cohort_customers` in tooltips.

For cancellations, create a separate table from `cancellations_monthly.csv`; do not subtract cancellation rows from revenue unless explicitly building a different net-sales definition and documenting it.

## 5. Report pages

### Page 1 — Executive Overview
- KPI cards: Revenue GBP, Orders, Average Order Value GBP, Units Sold, Known Customers
- Line chart: monthly revenue (dim_date year-month or `monthly_sales.csv`)
- Column chart: orders by month
- Slicers: country, year-month

### Page 2 — Product & Geography
- Bar chart: top products by revenue using `product_sales_top100.csv`
- Bar chart: top countries by revenue using `country_sales.csv`
- Table: product description, revenue, units, orders
- Slicer: country

### Page 3 — Customer Retention
- Matrix: cohort month × month index with retention_rate conditional formatting
- KPI cards: known customers and average order value
- Text box stating cohort month is the customer’s first observed purchase month in this dataset

### Page 4 — Returns & Data Quality (optional)
- Bar chart: cancellation/return lines by invoice month
- Cards from `data/processed/data_quality_report.json`: source rows, valid sales lines, excluded rows, missing customer IDs

## 6. Validation checklist
- Revenue equals the sum of `line_revenue` in `fact_sales.csv`.
- Orders count distinct invoice numbers, not transaction lines.
- UnitPrice is GBP in the source.
- Cancellation invoices starting with C and negative-quantity lines are excluded from positive-sales KPIs and separately reported.
- Customer cohort retention uses only rows with identified CustomerID.
- Date filters should use a date-only relationship, not invoice timestamp to calendar date.

Save as `Retail_Sales_Customer_Analytics.pbix`. The supplied package does not contain a `.pbix` file because Power BI Desktop must create and save the native report.
