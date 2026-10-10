import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 乱数のシードを固定（毎回同じデータが生成されるようにする）
np.random.seed(42)

# ---- 1. 設定値の定義 ----
NUM_CUSTOMERS = 1000  # 顧客数
NUM_PRODUCTS = 50     # 商品数
NUM_SALES = 20000     # 売上レコード数（トランザクション）

print("疑似データの生成を開始します...")

# ---- 2. 顧客マスタ (dim_customers) の生成 ----
customer_ids = [f"CUST_{i:04d}" for i in range(1, NUM_CUSTOMERS + 1)]
genders = np.random.choice(["Male", "Female", "Unknown"], size=NUM_CUSTOMERS, p=[0.45, 0.50, 0.05])
prefectures = np.random.choice(
    ["Tokyo", "Osaka", "Kanagawa", "Aichi", "Fukuoka", "Hokkaido", "Chiba", "Saitama"], 
    size=NUM_CUSTOMERS, 
    p=[0.30, 0.15, 0.15, 0.10, 0.10, 0.08, 0.06, 0.06] # 人口比率を意識
)
ages = np.random.randint(18, 65, size=NUM_CUSTOMERS)

df_customers = pd.DataFrame({
    "customer_id": customer_ids,
    "gender": genders,
    "age": ages,
    "prefecture": prefectures
})

# ---- 3. 商品マスタ (dim_products) の生成 ----
product_categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Home & Kitchen": ["Coffee Maker", "Toaster", "Blender", "Vacuum Cleaner"],
    "Books": ["Fiction", "Business", "Tech", "Comic"]
}

product_list = []
product_id_counter = 1

for category, items in product_categories.items():
    for item in items:
        # カテゴリごとに大体の価格帯を決める
        if category == "Electronics":
            price = np.random.randint(5000, 100000)
        elif category == "Apparel":
            price = np.random.randint(2000, 15000)
        elif category == "Home & Kitchen":
            price = np.random.randint(3000, 30000)
        else:
            price = np.random.randint(1000, 4000)
            
        product_list.append({
            "product_id": f"PROD_{product_id_counter:03d}",
            "product_name": item,
            "category": category,
            "price": price
        })
        product_id_counter += 1

# 指定した件数（50件）になるまで調整
df_products = pd.DataFrame(product_list[:NUM_PRODUCTS])

# ---- 4. 売上実績 (fact_sales) の生成 ----
# 過去1年間の日付をランダムに生成
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

random_days = np.random.randint(0, days_between_dates, size=NUM_SALES)
sales_dates = [start_date + timedelta(days=int(d)) for d in random_days]

# 既存のマスタからランダムにIDを紐づけ
chosen_customers = np.random.choice(df_customers["customer_id"], size=NUM_SALES)
chosen_products = np.random.choice(df_products["product_id"], size=NUM_SALES)
quantities = np.random.choice([1, 2, 3, 4, 5], size=NUM_SALES, p=[0.7, 0.15, 0.08, 0.05, 0.02])

df_sales = pd.DataFrame({
    "sales_id": [f"SALE_{i:06d}" for i in range(1, NUM_SALES + 1)],
    "sales_date": sales_dates,
    "customer_id": chosen_customers,
    "product_id": chosen_products,
    "quantity": quantities
})

# 価格をマスタから結合して合計金額を計算
df_sales = df_sales.merge(df_products[["product_id", "price"]], on="product_id", how="left")
df_sales["total_amount"] = df_sales["price"] * df_sales["quantity"]
df_sales = df_sales.drop(columns=["price"]) # 不要になった単価カラムを削除

print(f"データの生成が完了しました！")
print(f" - 売上データ: {len(df_sales)} 件")
print(f" - 顧客データ: {len(df_customers)} 件")
print(f" - 商品データ: {len(df_products)} 件")

# ---- 5. Databricksの raw_data（Bronze）に保存する ----
print("Databricksへの書き込みを開始します...")

# pandasのデータをDatabricksが扱える「Spark DataFrame」に変換して保存します
spark.createDataFrame(df_customers).write.mode("overwrite").saveAsTable("freelance_sandbox.raw_data.customers_raw")
spark.createDataFrame(df_products).write.mode("overwrite").saveAsTable("freelance_sandbox.raw_data.products_raw")
spark.createDataFrame(df_sales).write.mode("overwrite").saveAsTable("freelance_sandbox.raw_data.sales_raw")

print("Bronzeテーブルの作成がすべて成功しました！")