resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset_name
  friendly_name               = "Movies dataset"
  description                 = "Bigquery dataset for movies data processing."
  location                    = "US"

  labels = {
    environment = "default"
  }
}