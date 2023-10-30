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

resource "google_secret_manager_secret" "gcp_credentials_secret" {
  secret_id = "GCP_CREDENTIALS"  # Replace with your desired secret name

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "gcp_credentials_secret_version" {
  secret_id  = google_secret_manager_secret.gcp_credentials_secret.id
  secret_data = var.gcp_credentials
}

