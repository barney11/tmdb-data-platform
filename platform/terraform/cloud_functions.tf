provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_cloudfunctions_function" "extract_data_function" {
  name        = "extract-data-function"
  runtime     = "python38"
  trigger_http = true
  entry_point = "extract_data_function"
  available_memory_mb = 256
  source_repository {
    url = https://github.com/barney11/tmdb-data-platform/tree/main/platform
  }
}

resource "google_cloudfunctions_function" "migrate_data_function" {
  name        = "migrate-data-function"
  runtime     = "python38"
  trigger_http = true
  entry_point = "migrate_data_function"
  available_memory_mb = 256
  source_repository {
    url = https://github.com/barney11/tmdb-data-platform/tree/main/platform
  }
}

resource "google_cloudfunctions_function" "transform_data_function" {
  name        = "transform-data-function"
  runtime     = "python38"
  trigger_http = true
  entry_point = "transform_data_function"
  available_memory_mb = 256
  source_repository {
    url = https://github.com/barney11/tmdb-data-platform/tree/main/platform
  }
}

resource "google_cloud_workflows_workflow" "tmdb_workflow" {
  name        = "tmdb-workflow"
  source_contents = file("platform/workflows/tmdb_data_workflow.yaml")
  description = "TMDb data workflow"
}
