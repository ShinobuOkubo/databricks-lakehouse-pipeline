-- =====================================================================
-- お客様データのクレンジングと型安全性の確保
-- =====================================================================

-- =====================================================================
-- STEP 1: テーブルの存在保証（なければ空テーブルを作成、あればスキップ）
-- =====================================================================
CREATE TABLE IF NOT EXISTS freelance_sandbox.cleaned_data.sales_cleaned (
    sales_id STRING,
    sales_date DATE,
    customer_id STRING,
    product_id STRING,
    quantity INT,
    total_amount INT,
    updated_at TIMESTAMP
) USING DELTA;

CREATE TABLE IF NOT EXISTS freelance_sandbox.cleaned_data.customers_cleaned (
    customer_id STRING,
    gender STRING,
    age INT,
    prefecture STRING,
    updated_at TIMESTAMP
) USING DELTA;

CREATE TABLE IF NOT EXISTS freelance_sandbox.cleaned_data.products_cleaned (
    product_id STRING,
    product_name STRING,
    category STRING,
    price INT,
    updated_at TIMESTAMP
) USING DELTA;


-- =====================================================================
-- STEP 2: MERGE INTO による差分更新 (Upsert)
-- =====================================================================

-- 1. 売上実績
MERGE INTO freelance_sandbox.cleaned_data.sales_cleaned AS target
USING (
    SELECT
        CAST(sales_id AS STRING)       AS sales_id,
        CAST(sales_date AS DATE)       AS sales_date,
        CAST(customer_id AS STRING)    AS customer_id,
        CAST(product_id AS STRING)     AS product_id,
        CAST(quantity AS INT)          AS quantity,
        CAST(total_amount AS INT)      AS total_amount,
        CAST(updated_at AS TIMESTAMP)  AS updated_at
    FROM freelance_sandbox.cleaned_data.sales_pre_cleaned
) AS source
ON target.sales_id = source.sales_id
WHEN MATCHED THEN
  UPDATE SET
    target.sales_date  = source.sales_date,
    target.customer_id = source.customer_id,
    target.product_id  = source.product_id,
    target.quantity    = source.quantity,
    target.total_amount = source.total_amount,
    target.updated_at  = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (sales_id, sales_date, customer_id, product_id, quantity, total_amount, updated_at)
  VALUES (source.sales_id, source.sales_date, source.customer_id, source.product_id, source.quantity, source.total_amount, source.updated_at);

-- 2. 顧客マスタ
MERGE INTO freelance_sandbox.cleaned_data.customers_cleaned AS target
USING (
    SELECT
        CAST(customer_id AS STRING)    AS customer_id,
        TRIM(gender)                   AS gender,
        CAST(age AS INT)               AS age,
        TRIM(prefecture)               AS prefecture,
        CAST(updated_at AS TIMESTAMP)  AS updated_at
    FROM freelance_sandbox.cleaned_data.customers_pre_cleaned
) AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
  UPDATE SET
    target.gender     = source.gender,
    target.age        = source.age,
    target.prefecture = source.prefecture,
    target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (customer_id, gender, age, prefecture, updated_at)
  VALUES (source.customer_id, source.gender, source.age, source.prefecture, source.updated_at);

-- 3. 商品マスタ
MERGE INTO freelance_sandbox.cleaned_data.products_cleaned AS target
USING (
    SELECT
        CAST(product_id AS STRING)     AS product_id,
        TRIM(product_name)             AS product_name,
        TRIM(category)                 AS category,
        CAST(price AS INT)             AS price,
        CAST(updated_at AS TIMESTAMP)  AS updated_at
    FROM freelance_sandbox.cleaned_data.products_pre_cleaned
) AS source
ON target.product_id = source.product_id
WHEN MATCHED THEN
  UPDATE SET
    target.product_name = source.product_name,
    target.category     = source.category,
    target.price        = source.price,
    target.updated_at   = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (product_id, product_name, category, price, updated_at)
  VALUES (source.product_id, source.product_name, source.category, source.price, source.updated_at);
