resource "google_cloud_scheduler_job" "tmdb_data_workflow_scheduler" {
  name        = "tmdb-data-workflow-scheduler"
  description = "Workflow scheduler for movies data processing."
  schedule    = "0 9 * * *"  # Trigger at 9:00 AM every day (UTC time)

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/movies-data-platform/locations/us-central1/workflows/tmdb-data-workflow/executions"
    oauth_token {
      service_account_email = "service-account@movies-data-platform.iam.gserviceaccount.com"
    }
  }

  time_zone = "Europe/Paris"

  retry_config {
    retry_count = 3
  }

}
