resource "google_secret_manager_secret" "tmdb_api_key_secret" {
  secret_id = "TMDB_API_KEY"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "tmdb_api_key_secret_version" {
  secret = google_secret_manager_secret.tmdb_api_key_secret.id
  secret_data = var.tmdb_api_key
}

resource "google_secret_manager_secret" "gcp_credentials_secret" {
  secret_id = "GCP_CREDENTIALS_JSON"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "gcp_credentials_secret_version" {
  secret = google_secret_manager_secret.gcp_credentials_secret.id
  secret_data = file(var.gcp_credentials_json)
}