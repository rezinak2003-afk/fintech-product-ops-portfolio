-- Long-form monthly cohort retention. Customer month is derived from first identified order month.
WITH customer_months AS (
 SELECT customer_id, substr(invoice_date,1,7) AS order_month
 FROM sales WHERE customer_id IS NOT NULL
 GROUP BY customer_id, substr(invoice_date,1,7)
), cohorts AS (
 SELECT customer_id, MIN(order_month) AS cohort_month FROM customer_months GROUP BY customer_id
), joined AS (
 SELECT c.cohort_month, o.order_month, o.customer_id,
        (CAST(substr(o.order_month,1,4) AS INTEGER)*12+CAST(substr(o.order_month,6,2) AS INTEGER))-
        (CAST(substr(c.cohort_month,1,4) AS INTEGER)*12+CAST(substr(c.cohort_month,6,2) AS INTEGER)) AS period_index
 FROM customer_months o JOIN cohorts c ON o.customer_id=c.customer_id
), active AS (
 SELECT cohort_month, period_index, COUNT(DISTINCT customer_id) AS active_customers
 FROM joined GROUP BY cohort_month, period_index
), sizes AS (
 SELECT cohort_month, active_customers AS cohort_size FROM active WHERE period_index=0
)
SELECT a.cohort_month, s.cohort_size, a.period_index, a.active_customers,
       ROUND(100.0*a.active_customers/s.cohort_size,1) AS retention_pct
FROM active a JOIN sizes s USING(cohort_month)
WHERE a.period_index BETWEEN 0 AND 12
ORDER BY a.cohort_month,a.period_index;
