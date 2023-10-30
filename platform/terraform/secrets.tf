provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_secret_manager_secret" "tmdb_api_key_secret" {
  secret_id = "TMDB_API_KEY"  # Replace with your desired secret name

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "tmdb_api_key_secret_version" {
  secret_id  = google_secret_manager_secret.tmdb_api_key_secret.id
  secret_data = var.tmdb_api_key
}
