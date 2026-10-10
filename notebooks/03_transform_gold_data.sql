-- =====================================================================
-- 1. 顧客マスタ (dim_customers) の作成
-- =====================================================================
-- cleaned_data からデータを取得し、ec_sales_analytics スキーマに最終的なマスタを作成します
CREATE OR REPLACE TABLE freelance_sandbox.ec_sales_analytics.dim_customers AS
SELECT 
    customer_id,
    gender,
    age,
    prefecture
FROM 
    freelance_sandbox.cleaned_data.customers_cleaned;

-- =====================================================================
-- 2. 商品マスタ (dim_products) の作成
-- =====================================================================
CREATE OR REPLACE TABLE freelance_sandbox.ec_sales_analytics.dim_products AS
SELECT 
    product_id,
    product_name,
    category,
    price
FROM 
    freelance_sandbox.cleaned_data.products_cleaned;

-- =====================================================================
-- 3. 売上実績 (fact_sales) の作成
-- =====================================================================
CREATE OR REPLACE TABLE freelance_sandbox.ec_sales_analytics.fact_sales AS
SELECT 
    sales_id,
    sales_date,
    customer_id,
    product_id,
    quantity,
    total_amount
FROM 
    freelance_sandbox.cleaned_data.sales_cleaned;