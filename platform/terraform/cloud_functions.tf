# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
  type        = "zip"
  output_path = "/tmp/${var.archive_name}.zip"
  source_dir  = ".."
  excludes     = var.excludes
}

# Add source code zip to the Cloud Function's bucket (Cloud_function_bucket) 
resource "google_storage_bucket" "cloud_functions_bucket" {
  name = var.cloud_functions_bucket_name
  project = var.project_id
  location = var.cloud_functions_bucket_location
  force_destroy = true
  uniform_bucket_level_access = true
  storage_class = var.bucket_storage_class

  versioning {
    enabled = var.bucket_versioning
  }
}

resource "google_storage_bucket_object" "cloud_functions_bucket_object" {
  name   = "${var.cloud_functions_bucket_name}.${data.archive_file.source.output_sha}.zip"
  bucket = google_storage_bucket.cloud_functions_bucket.id
  source = data.archive_file.source.output_path
}

# Data extraction cloud function
resource "google_cloudfunctions_function" "extract_data_cloudfunction" {
  name        = "extract-data-cloudfunction"
  runtime     = "python38"
  trigger_http = true
  entry_point = "extract_data_function"
  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.cloud_functions_bucket.id
  source_archive_object = google_storage_bucket_object.cloud_functions_bucket_object.name
  environment_variables = {
    TF_VAR_PROJECT_ID = var.project_id
    TF_VAR_PROJECT_NUMBER = var.project_number
    TF_VAR_DATASET_NAME = var.dataset_name
    TF_VAR_DATA_STORAGE_BUCKET_NAME = var.data_storage_bucket_name
  }
}

# Data migration cloud function
resource "google_cloudfunctions_function" "migrate_data_cloudfunction" {
  name        = "migrate-data-cloudfunction"
  runtime     = "python38"
  trigger_http = true
  entry_point = "migrate_data_function"
  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.cloud_functions_bucket.id
  source_archive_object = google_storage_bucket_object.cloud_functions_bucket_object.name
  environment_variables = {
    TF_VAR_PROJECT_ID = var.project_id
    TF_VAR_PROJECT_NUMBER = var.project_number
    TF_VAR_DATASET_NAME = var.dataset_name
    TF_VAR_DATA_STORAGE_BUCKET_NAME = var.data_storage_bucket_name
  }
}

# Data transformation cloud function
resource "google_cloudfunctions_function" "transform_data_cloudfunction" {
  name        = "transform-data-cloudfunction"
  runtime     = "python38"
  trigger_http = true
  entry_point = "transform_data_function"
  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.cloud_functions_bucket.id
  source_archive_object = google_storage_bucket_object.cloud_functions_bucket_object.name
  environment_variables = {
    TF_VAR_PROJECT_ID = var.project_id
    TF_VAR_PROJECT_NUMBER = var.project_number
    TF_VAR_DATASET_NAME = var.dataset_name
    TF_VAR_DATA_STORAGE_BUCKET_NAME = var.data_storage_bucket_name
  }
}

# Data workflow to run the above cloud functions sequentially
resource "google_workflows_workflow" "tmdb_data_workflow" {
  name        = "tmdb-data-workflow"
  source_contents = file("../workflows/tmdb_data_workflow.yaml")
  description = "TMDb data workflow"
}
