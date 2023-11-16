# Cloud storage bucket for raw data
resource "google_storage_bucket" "movies_bucket_11" {
  name          = var.data_storage_bucket_name
  location      = var.region
}

# Cloud storage bucket for terraform states
resource "google_storage_bucket" "movies_data_platform_terraform_states_11"  {
  name          = var.terraform_states_bucket_name
  location      = var.region
}
