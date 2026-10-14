# Data dictionary

| File | Grain | Key fields / measures | Purpose |
|---|---|---|---|
| `fact_sales.csv` | One eligible sale line | invoice_no, stock_code, invoice_date, invoice_date_date, customer_id, line_revenue | Sales facts; cancellations removed |
| `dim_customer.csv` | One identified customer | customer_id, first_purchase_date, cohort_month | Cohort attributes |
| `dim_product.csv` | One stock-code/description combination | stock_code, description | Product labels |
| `dim_date.csv` | One calendar date | date, year, month_number, month_name, year_month, quarter | Calendar slicing |
| `monthly_sales.csv` | One invoice month | revenue_gbp, orders, units_sold, avg_order_value_gbp | Trend report |
| `country_sales.csv` | One country | revenue_gbp, orders, units_sold | Geographic comparison |
| `product_sales_top100.csv` | One product code/description | revenue_gbp, orders, units_sold | Top product visual |
| `monthly_cohort_retention.csv` | Cohort month × months since first purchase | cohort_customers, active_customers, retention_rate | Retention matrix |
| `cancellations.csv` | One cancellation/negative-quantity line | invoice_no, quantity, unit_price, invoice_date | Separate returns/cancellations review |
| `cancellations_monthly.csv` | One month with cancellation/return activity | cancel_or_return_lines, cancel_or_return_invoices | Time series |

## Metric definitions
- **Revenue GBP:** sum of quantity × unit price over eligible sales lines.
- **Orders:** distinct invoice numbers among eligible sales lines.
- **Average order value (AOV):** revenue / distinct eligible invoices.
- **Identified customers:** distinct non-missing customer IDs in the eligible sales lines.
- **Cohort month:** calendar month of the customer's first observed eligible purchase.
- **Retention rate:** distinct cohort customers with eligible activity in month index N ÷ distinct customers in the cohort month.
- **Cancellation/return lines:** records whose invoice number starts with C or whose quantity is negative. Counts are line-level and may include both kinds of records; this is not a refund-value metric.
