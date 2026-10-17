variable "catalog_name" {
  type        = string
  default     = "freelance_sandbox"
  description = "Databricksのカタログ名"
}

variable "bronze_schema" {
  type    = string
  default = "raw_data"
}

variable "silver_schema" {
  type    = string
  default = "cleaned_data"
}

variable "gold_schema" {
  type    = string
  default = "ec_sales_analytics"
}