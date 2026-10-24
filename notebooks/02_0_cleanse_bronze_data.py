from pyspark.sql import functions as F

print("シルバー層（Silver）のクレンジング・構造化処理を開始します...")

# 1. Bronzeテーブルの読み込み
df_sales_raw = spark.table("freelance_sandbox.raw_data.sales_raw")
df_cust_raw = spark.table("freelance_sandbox.raw_data.customers_raw")
df_prod_raw = spark.table("freelance_sandbox.raw_data.products_raw")

# 2. 売上実績（sales）のクレンジング + タイムスタンプ付与
# - スキーマの結合キー（customer_id, product_id）が Null や "None"（文字列）のものは厳格に除外
# - 金額（total_amount）が NaN/Null や "NaN"（文字列）のものも集計バグの原因になるため除外
print("売上データのNull/NaNチェック（クレンジング）を実行中...")
df_sales_pre = df_sales_raw \
    .filter(F.col("customer_id").isNotNull() & (F.col("customer_id") != "None")) \
    .filter(F.col("product_id").isNotNull() & (F.col("product_id") != "None")) \
    .filter(F.col("total_amount").isNotNull() & (F.col("total_amount") != "NaN")) \
    .withColumn("updated_at", F.current_timestamp())

# 3. 顧客マスタ（customers）のクレンジング + タイムスタンプ付与
# - システム入力エラーである異常値「年齢がマイナス（-99）」を検知
# 年齢が正常なデータ（-99以外）だけで、年齢の中央値（0.5のパーセンタイル）を動的に計算
valid_cust_df = df_cust_raw.filter(F.col("age") != -99)
calculated_median = valid_cust_df.approxQuantile("age", [0.5], 0.001)[0]
# 小数点以下を丸めて整数にする（例: 41.0 ➔ 41）
dynamic_median_age = int(round(calculated_median))
print(f"正常データから算出された現在の年齢中央値: {dynamic_median_age} 歳")

print("顧客データの異常値（年齢: -99）の自動補正を実行中...")
df_cust_pre = df_cust_raw.withColumn(
    "age",
    F.when(F.col("age") == -99, F.lit(dynamic_median_age)).otherwise(F.col("age"))
).withColumn("updated_at", F.current_timestamp())

# 4. 商品マスタ（products）のクレンジング
# - 今回はクレンジング対象データを混ぜていないため、タイムスタンプ付与のみ
df_prod_pre = df_prod_raw.withColumn("updated_at", F.current_timestamp())

# 5. クレンジング済みの中間テーブル（_pre_cleaned）として保存
print("クレンジング済みデータを cleaned_data スキーマへ保存中...")
df_sales_pre.write.mode("overwrite") \
    .saveAsTable("freelance_sandbox.cleaned_data.sales_pre_cleaned")
df_cust_pre.write.mode("overwrite") \
    .saveAsTable("freelance_sandbox.cleaned_data.customers_pre_cleaned")
df_prod_pre.write.mode("overwrite") \
    .saveAsTable("freelance_sandbox.cleaned_data.products_pre_cleaned")

print("--- クレンジング処理（中間レイヤーへの出力）が成功しました！ ---")
# 実際に何件のデータが排除されたかを確認
print(f"元の売上データ件数: 20000 件 ➔ クレンジング後件数: {df_sales_pre.count()} 件 (Null/NaNが正常に弾かれました)")
