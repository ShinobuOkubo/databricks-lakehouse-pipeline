terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0" # 2026年現在の安定版を指定
    }
  }
}

# Databricksへの接続設定（認証情報はbatファイルにて、環境変数から自動読み込みさせるため空でOK）
provider "databricks" {}