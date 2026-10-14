-- RFM-style segments: recency (days since last order), frequency (distinct invoices), monetary value.
WITH customer_base AS (
 SELECT customer_id, MAX(date(invoice_date)) AS last_order,
        COUNT(DISTINCT invoice) AS frequency,
        SUM(revenue_gbp) AS monetary
 FROM sales WHERE customer_id IS NOT NULL GROUP BY customer_id
), snapshot AS (SELECT date(MAX(invoice_date), '+1 day') AS snapshot_date FROM sales),
scored AS (
 SELECT c.*,
        CAST(julianday(s.snapshot_date)-julianday(c.last_order) AS INTEGER) AS recency_days,
        6-NTILE(5) OVER (ORDER BY CAST(julianday(s.snapshot_date)-julianday(c.last_order) AS INTEGER)) AS r_score,
        NTILE(5) OVER (ORDER BY frequency, customer_id) AS f_score
 FROM customer_base c CROSS JOIN snapshot s
), segments AS (
 SELECT *, CASE
  WHEN r_score>=4 AND f_score>=4 THEN 'Champions'
  WHEN r_score>=3 AND f_score>=3 THEN 'Loyal Customers'
  WHEN r_score>=4 AND f_score<=2 THEN 'New / Potential Loyalists'
  WHEN r_score>=3 AND f_score<=2 THEN 'Promising'
  WHEN r_score<=2 AND f_score>=3 THEN 'At Risk'
  WHEN r_score<=2 AND f_score>=2 THEN 'Hibernating'
  ELSE 'Lost' END AS segment
 FROM scored
)
SELECT segment, COUNT(*) AS customers,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) AS pct_customers,
       ROUND(SUM(monetary),2) AS revenue_gbp,
       ROUND(100.0*SUM(monetary)/SUM(SUM(monetary)) OVER (),1) AS pct_revenue
FROM segments GROUP BY segment ORDER BY revenue_gbp DESC;
