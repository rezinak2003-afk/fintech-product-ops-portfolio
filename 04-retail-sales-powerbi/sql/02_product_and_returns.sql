-- Top products by value and volume.
SELECT stock_code, MAX(description) AS description,
       SUM(quantity) AS units_sold, ROUND(SUM(revenue_gbp),2) AS revenue_gbp
FROM sales GROUP BY stock_code ORDER BY revenue_gbp DESC LIMIT 20;

-- Monthly return/cancellation value as a share of sales.
WITH s AS (SELECT substr(invoice_date,1,7) AS month, SUM(revenue_gbp) AS sales_gbp FROM sales GROUP BY 1),
r AS (SELECT substr(invoice_date,1,7) AS month, SUM(return_value_gbp) AS returns_gbp FROM returns GROUP BY 1)
SELECT s.month, ROUND(s.sales_gbp,2) AS sales_gbp,
       ROUND(COALESCE(r.returns_gbp,0),2) AS returns_gbp,
       ROUND(100.0*COALESCE(r.returns_gbp,0)/NULLIF(s.sales_gbp,0),2) AS return_rate_pct
FROM s LEFT JOIN r USING(month) ORDER BY s.month;
