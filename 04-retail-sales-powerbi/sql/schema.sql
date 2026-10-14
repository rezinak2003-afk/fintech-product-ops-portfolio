-- SQLite schema for cleaned Online Retail II sales/returns.
CREATE TABLE IF NOT EXISTS sales (
  invoice TEXT NOT NULL,
  stock_code TEXT,
  description TEXT,
  quantity INTEGER NOT NULL,
  invoice_date TEXT NOT NULL,
  unit_price REAL NOT NULL,
  customer_id TEXT,
  country TEXT,
  revenue_gbp REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS returns (
  invoice TEXT NOT NULL,
  stock_code TEXT,
  description TEXT,
  quantity INTEGER NOT NULL,
  invoice_date TEXT NOT NULL,
  unit_price REAL NOT NULL,
  customer_id TEXT,
  country TEXT,
  return_value_gbp REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(invoice_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id);
