import pandas as pd

# S3のオブジェクトURLを直接指定します
s3_sales_url     = "https://"
s3_customers_url = "https://"
s3_products_url  = "https://"

print("S3からデータを読み込んでいます...")
pdf_sales = pd.read_csv(s3_sales_url)
pdf_customers = pd.read_csv(s3_customers_url)
pdf_products = pd.read_csv(s3_products_url)

df_sales_bronze = spark.createDataFrame(pdf_sales)
df_customers_bronze = spark.createDataFrame(pdf_customers)
df_products_bronze = spark.createDataFrame(pdf_products)

print("Bronzeテーブルへ上書き保存中...")

df_sales_bronze.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("freelance_sandbox.raw_data.sales_raw")

df_customers_bronze.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("freelance_sandbox.raw_data.customers_raw")

df_products_bronze.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("freelance_sandbox.raw_data.products_raw")

print("--- ロードに成功しました ---")
print(f"売上実績件数: {df_sales_bronze.count()} 件")
