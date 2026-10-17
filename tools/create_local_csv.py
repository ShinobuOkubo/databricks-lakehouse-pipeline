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
    p=[0.30, 0.15, 0.15, 0.10, 0.10, 0.08, 0.06, 0.06]
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

df_products = pd.DataFrame(product_list[:NUM_PRODUCTS])

# ---- 4. 売上実績 (fact_sales) の生成 ----
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

random_days = np.random.randint(0, days_between_dates, size=NUM_SALES)
sales_dates = [start_date + timedelta(days=int(d)) for d in random_days]

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

df_sales = df_sales.merge(df_products[["product_id", "price"]], on="product_id", how="left")
df_sales["total_amount"] = df_sales["price"] * df_sales["quantity"]
df_sales = df_sales.drop(columns=["price"])

# =====================================================================
# [追加] カオスデータの意図的インジェクション (テスト用欠損・異常値)
# =====================================================================
print("テスト用の欠損値（NaN/Null）と異常値をデータに注入しています...")

# ① 売上データ: 200件の売上金額(total_amount)を NaN にする（売上集計バグのシミュレート）
nan_sales_indices = np.random.choice(df_sales.index, size=200, replace=False)
df_sales.loc[nan_sales_indices, "total_amount"] = np.nan

# ② 売上データ: 100件の customer_id を None (Null) にする（マスタ未登録バグのシミュレート）
null_cust_indices = np.random.choice(df_sales.index, size=100, replace=False)
df_sales.loc[null_cust_indices, "customer_id"] = None

# ③ 顧客データ: 50件の年齢(age)を「マイナス値」にする（システム入力エラーのシミュレート）
invalid_age_indices = np.random.choice(df_customers.index, size=50, replace=False)
df_customers.loc[invalid_age_indices, "age"] = -99

# ローカルにCSVとして保存
# 顧客マスタ
df_customers.to_csv("./customers_raw_dirty.csv", index=False)
# 商品マスタ
df_products.to_csv("./products.csv", index=False)
#  売上実績
df_sales.to_csv("./sales_raw_dirty.csv", index=False)
