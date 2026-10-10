-- =====================================================================
-- お客様データのクレンジングと型安全性の確保
-- =====================================================================
CREATE OR REPLACE TABLE freelance_sandbox.cleaned_data.customers_cleaned AS
SELECT 
    CAST(customer_id AS STRING) AS customer_id, -- 明示的な型定義
    TRIM(gender) AS gender,                      -- 前後空白の削除（実務の癖付け）
    CAST(age AS INT) AS age,
    TRIM(prefecture) AS prefecture
FROM 
    freelance_sandbox.raw_data.customers_raw;

CREATE OR REPLACE TABLE freelance_sandbox.cleaned_data.products_cleaned AS
SELECT 
    CAST(product_id AS STRING) AS product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    CAST(price AS INT) AS price
FROM 
    freelance_sandbox.raw_data.products_raw;

CREATE OR REPLACE TABLE freelance_sandbox.cleaned_data.sales_cleaned AS
SELECT 
    CAST(sales_id AS STRING) AS sales_id,
    CAST(sales_date AS DATE) AS sales_date, -- ここでDATE型に変換
    CAST(customer_id AS STRING) AS customer_id,
    CAST(product_id AS STRING) AS product_id,
    CAST(quantity AS INT) AS quantity,
    CAST(total_amount AS INT) AS total_amount
FROM 
    freelance_sandbox.raw_data.sales_raw;