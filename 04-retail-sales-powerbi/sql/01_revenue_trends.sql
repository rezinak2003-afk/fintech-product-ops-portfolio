-- Monthly revenue, invoice count and month-over-month change.
WITH monthly AS (
  SELECT substr(invoice_date,1,7) AS month,
         SUM(revenue_gbp) AS revenue_gbp,
         COUNT(DISTINCT invoice) AS invoices
  FROM sales
  GROUP BY 1
), lagged AS (
  SELECT month, revenue_gbp, invoices,
         LAG(revenue_gbp) OVER (ORDER BY month) AS previous_month_revenue
  FROM monthly
)
SELECT month, ROUND(revenue_gbp,2) AS revenue_gbp, invoices,
       ROUND(100.0*(revenue_gbp-previous_month_revenue)/NULLIF(previous_month_revenue,0),1) AS mom_growth_pct
FROM lagged ORDER BY month;

-- Country mix and contribution to total revenue.
WITH c AS (SELECT country, SUM(revenue_gbp) AS revenue_gbp FROM sales GROUP BY country)
SELECT country, ROUND(revenue_gbp,2) AS revenue_gbp,
       ROUND(100.0*revenue_gbp/SUM(revenue_gbp) OVER (),2) AS pct_of_total
FROM c ORDER BY revenue_gbp DESC;
