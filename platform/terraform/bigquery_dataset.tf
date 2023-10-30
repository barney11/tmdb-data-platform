provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_bigquery_dataset" "tmdb_dataset" {
  dataset_id                  = "tmdb_dataset"
  friendly_name               = "Movies dataset"
  description                 = "Bigquery dataset for movies data processing."
  location                    = "US"

  labels = {
    environment = "default"
  }
  
  default_table_expiration_ms = 3600000  # 1 hour in milliseconds
  default_partition_expiration_ms = 2592000000  # 30 days in milliseconds
}