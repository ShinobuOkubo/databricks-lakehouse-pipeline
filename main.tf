# 開発用のカタログを作成（Databricks内でデータを分離するトップ階層）
# resource "databricks_catalog" "sandbox" {
#   name    = var.catalog_name
#   comment = "フリーランス研究開発用のデータカタログ"
# }

# 1. Bronze処理に使用するスキーマ
resource "databricks_schema" "bronze" {
  # 無料版では、カタログを手動で作成する必要がある
  # catalog_name = databricks_catalog.sandbox.name
  catalog_name = var.catalog_name
  name         = var.bronze_schema
  comment      = "生データをそのまま保管する場所"
}

# 2. Silver処理に使用するスキーマ
resource "databricks_schema" "silver" {
  catalog_name = var.catalog_name
  name         = var.silver_schema
  comment      = "クレンジング、データ型の整形、重複排除、フィルタリングを行った信頼できるデータ"
}

# 3. Gold処理に使用するスキーマ
resource "databricks_schema" "gold" {
  catalog_name = var.catalog_name
  name         = var.gold_schema
  comment      = "ECサイトの売上・顧客分析用データモデル"
}