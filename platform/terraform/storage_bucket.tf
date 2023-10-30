provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "movies_bucket_11" {
  name          = "movies-bucket-11"
  location      = var.region
}
